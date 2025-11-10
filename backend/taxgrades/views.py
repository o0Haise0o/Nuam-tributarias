from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Calificacion
from .serializers import CalificacionSerializer
from django.db import transaction
from django.http import HttpResponse

import csv, io

from .models import TaxGrade, Calificacion, OrigenInformacion, AuditLog
from .serializers import (
    TaxGradeSerializer,
    CalificacionSerializer,
    OrigenInformacionSerializer,
    AuditLogSerializer,
)

def _current_user_str(request):
    return (getattr(request, "user", None) and getattr(request.user, "username", "")) or "manual"



class TaxGradeViewSet(viewsets.ModelViewSet):
    queryset = TaxGrade.objects.all()
    serializer_class = TaxGradeSerializer



class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.select_related("origen").all()
    serializer_class = CalificacionSerializer


    filterset_fields = {
        "mercado": ["exact"],
        "habilitado": ["exact"],
        "periodo_comercial": ["exact", "gte", "lte"],
        "instrumento": ["exact"],
        "origen": ["exact"],
    }
    search_fields = ["instrumento", "descripcion", "origen_texto", "secuencia_evento"]
    ordering_fields = ["periodo_comercial", "instrumento", "monto", "dividendo", "updated_at"]

    def perform_create(self, serializer):
        obj = serializer.save()
        AuditLog.objects.create(
            entity="Calificacion",
            entity_id=str(obj.pk),
            action="create",
            user=_current_user_str(self.request),
            after=CalificacionSerializer(obj).data,
            origen=obj.origen,
        )

    def perform_update(self, serializer):
        before = CalificacionSerializer(self.get_object()).data
        obj = serializer.save()
        after = CalificacionSerializer(obj).data
        AuditLog.objects.create(
            entity="Calificacion",
            entity_id=str(obj.pk),
            action="update",
            user=_current_user_str(self.request),
            before=before,
            after=after,
            origen=obj.origen,
        )

    def perform_destroy(self, instance):
        before = CalificacionSerializer(instance).data
        AuditLog.objects.create(
            entity="Calificacion",
            entity_id=str(instance.pk),
            action="delete",
            user=_current_user_str(self.request),
            before=before,
            origen=instance.origen,
        )
        instance.delete()



    @action(detail=False, methods=["post"], url_path="preview-csv", parser_classes=[MultiPartParser])
    def preview_csv(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"detail": "Adjunta un CSV en el campo 'file'."}, status=400)

        reader = csv.DictReader(io.TextIOWrapper(file, encoding="utf-8"))
        expected = {"mercado", "periodo_comercial", "instrumento", "monto"}
        if not expected.issubset(set([c.strip() for c in (reader.fieldnames or [])])):
            return Response({
                "detail": "Encabezados mínimos faltantes.",
                "esperado": sorted(list(expected)),
                "encontrado": reader.fieldnames,
            }, status=400)

        total = 0
        sample_rows, errors = [], []
        line = 1
        for row in reader:
            line += 1
            total += 1
            try:
                if not row.get("instrumento") or not row.get("periodo_comercial"):
                    raise ValueError("Falta 'instrumento' o 'periodo_comercial'")
                _ = float(row.get("monto", "0"))
            except Exception as ex:
                errors.append({"linea": line, "error": str(ex), "row": row})
            if len(sample_rows) < 10:
                sample_rows.append(row)

        return Response({
            "total_filas": total,
            "muestras": sample_rows,
            "errores": errors[:50],
            "ok": len(errors) == 0
        }, status=200)


    @action(detail=False, methods=["post"], url_path="bulk-upload", parser_classes=[MultiPartParser])
    def bulk_upload(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"detail": "Adjunta un archivo CSV en el campo 'file'."}, status=400)

        origen = OrigenInformacion.objects.create(
            fecha=request.data.get("fecha") or request.data.get("date") or request.data.get("fecha_carga"),
            archivo=file.name,
            tipo_ingreso="masivo",
            encargado=request.data.get("encargado", ""),
            observaciones=request.data.get("observaciones", ""),
            validado_formato=False,
        )

        created = 0
        errors = []
        reader = csv.DictReader(io.TextIOWrapper(file, encoding="utf-8"))
        expected = {"mercado", "periodo_comercial", "instrumento", "monto"}
        if not expected.issubset(set([c.strip() for c in reader.fieldnames or []])):
            return Response({
                "detail": "Encabezados mínimos faltantes.",
                "esperado": sorted(list(expected)),
                "encontrado": reader.fieldnames,
            }, status=400)

        items = []
        line = 1
        for row in reader:
            line += 1
            try:
                habilitado = str(row.get("habilitado", "true")).strip().lower() in ["1","true","t","yes","y","si","sí"]
                factor = row.get("factor") or "1"
                items.append(Calificacion(
                    mercado=row.get("mercado", "CL").strip(),
                    origen_texto=(row.get("origen_texto") or "").strip(),
                    periodo_comercial=row["periodo_comercial"],
                    instrumento=row["instrumento"].strip(),
                    fecha_pago=(row.get("fecha_pago") or None),
                    descripcion=row.get("descripcion", ""),
                    secuencia_evento=(row.get("secuencia_evento") or "").strip(),
                    monto=row.get("monto") or 0,
                    dividendo=row.get("dividendo") or 0,
                    habilitado=habilitado,
                    factor=factor,
                    origen=origen,
                ))
            except Exception as ex:
                errors.append({"linea": line, "error": str(ex), "row": row})

        if errors:
            origen.observaciones += f" | Errores: {len(errors)}"
            origen.save(update_fields=["observaciones"])
            return Response({"origen_id": origen.id, "errores": errors[:50]}, status=400)

        with transaction.atomic():
            Calificacion.objects.bulk_create(items, batch_size=1000)
            created = len(items)
            origen.validado_formato = True
            origen.save(update_fields=["validado_formato"])

        AuditLog.objects.create(
            entity="Calificacion",
            entity_id="*bulk*",
            action="bulk_import",
            user=_current_user_str(request),
            after={"origen_id": origen.id, "creados": created},
            origen=origen,
        )
        return Response({"origen_id": origen.id, "creados": created}, status=201)

 
    @action(detail=False, methods=["post"], url_path="cancelar-importacion")
    def cancelar_importacion(self, request):
        origen_id = request.data.get("origen_id")
        if not origen_id:
            return Response({"detail": "Debes enviar 'origen_id'."}, status=400)
        try:
            origen = OrigenInformacion.objects.get(pk=origen_id)
        except OrigenInformacion.DoesNotExist:
            return Response({"detail": "origen_id no encontrado."}, status=404)

        with transaction.atomic():
            count = origen.calificaciones.count()
            origen.calificaciones.all().delete()

        AuditLog.objects.create(
            entity="Calificacion",
            entity_id="*bulk*",
            action="cancel_import",
            user=_current_user_str(request),
            before={"origen_id": origen.id, "eliminadas": count},
            origen=origen,
        )
        return Response({"eliminadas": count, "origen_id": origen_id}, status=200)

    @action(detail=False, methods=["get"], url_path="export")
    def export(self, request):
        qs = self.filter_queryset(self.get_queryset())
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = 'attachment; filename="calificaciones.csv"'
        writer = csv.writer(response)
        writer.writerow([
            "id","mercado","origen_texto","periodo_comercial","instrumento","fecha_pago",
            "descripcion","secuencia_evento","monto","dividendo","habilitado","factor","origen_id"
        ])
        for c in qs.iterator():
            writer.writerow([
                c.id, c.mercado, c.origen_texto, c.periodo_comercial, c.instrumento, c.fecha_pago,
                c.descripcion, c.secuencia_evento, c.monto, c.dividendo, c.habilitado, c.factor,
                (c.origen_id or "")
            ])
        return response


class OrigenInformacionViewSet(viewsets.ModelViewSet):
    queryset = OrigenInformacion.objects.all()
    serializer_class = OrigenInformacionSerializer
    filterset_fields = ["tipo_ingreso", "validado_formato", "fecha"]
    search_fields = ["archivo", "encargado", "observaciones"]
    ordering_fields = ["fecha", "created_at"]



class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    filterset_fields = ["entity", "action", "user", "origen"]
    search_fields = ["entity_id", "user"]
    ordering_fields = ["timestamp"]
