from rest_framework import serializers
from .models import TaxGrade, Calificacion, OrigenInformacion, AuditLog

class TaxGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxGrade
        fields = "__all__"

class OrigenInformacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrigenInformacion
        fields = "__all__"

class CalificacionSerializer(serializers.ModelSerializer):
    origen = OrigenInformacionSerializer(read_only=True)
    origen_id = serializers.PrimaryKeyRelatedField(
        queryset=OrigenInformacion.objects.all(), write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Calificacion
        fields = [
            "id", "mercado", "origen_texto", "periodo_comercial", "instrumento", "fecha_pago",
            "descripcion", "secuencia_evento", "monto", "dividendo", "habilitado", "factor",
            "origen", "origen_id", "created_at", "updated_at",
        ]

    def validate(self, attrs):
        monto = attrs.get("monto", 0)
        factor = attrs.get("factor", 1)
        if monto is not None and monto < 0:
            raise serializers.ValidationError({"monto": "El monto no puede ser negativo."})
        if factor is not None and factor <= 0:
            raise serializers.ValidationError({"factor": "El factor debe ser mayor que 0."})
        return attrs
    
class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = "__all__"
