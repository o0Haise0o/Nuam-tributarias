from django.db import models
import uuid



MERCADOS = [
    ("CL", "Chile"),
    ("US", "USA"),
    ("EU", "Europa"),
]

TIPOS_INGRESO = [
    ("manual", "Manual"),
    ("import", "Importación"),
    ("masivo", "Carga masiva"),
]


class TaxGrade(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.name}"
    


class OrigenInformacion(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateField()
    archivo = models.CharField(max_length=255, blank=True)      # nombre de archivo fuente (si hubo)
    tipo_ingreso = models.CharField(max_length=10, choices=TIPOS_INGRESO, default="manual")
    encargado = models.CharField(max_length=120, blank=True)    # quién cargó
    observaciones = models.TextField(blank=True)

    validado_formato = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Origen de información"
        verbose_name_plural = "Orígenes de información"
        ordering = ["-fecha", "-id"]

    def __str__(self):
        return f"{self.fecha} / {self.tipo_ingreso} / {self.archivo or 'sin-archivo'}"


class Calificacion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    mercado = models.CharField(max_length=4, choices=MERCADOS)
    origen_texto = models.CharField(max_length=100, blank=True)
    periodo_comercial = models.DateField()
    instrumento = models.CharField(max_length=120)
    fecha_pago = models.DateField(null=True, blank=True)
    descripcion = models.TextField(blank=True)
    secuencia_evento = models.CharField(max_length=60, blank=True)

    monto = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    dividendo = models.DecimalField(max_digits=18, decimal_places=4, default=0)

    habilitado = models.BooleanField(default=True)
    factor = models.DecimalField(max_digits=12, decimal_places=6, default=1)

    origen = models.ForeignKey(
        OrigenInformacion,
        on_delete=models.PROTECT,
        related_name="calificaciones",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-periodo_comercial", "instrumento", "secuencia_evento"]
        indexes = [
            models.Index(fields=["periodo_comercial"]),
            models.Index(fields=["instrumento"]),
            models.Index(fields=["mercado"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["instrumento", "periodo_comercial", "secuencia_evento"],
                name="uq_calif_instrumento_periodo_secuencia",
                violation_error_message="Ya existe una calificación para ese instrumento/periodo/secuencia.",
            )
        ]

    def __str__(self):
        return f"{self.instrumento} ({self.periodo_comercial})"
    
class AuditLog(models.Model):
    entity = models.CharField(max_length=50)            
    entity_id = models.CharField(max_length=64)         
    action = models.CharField(max_length=30)            
    user = models.CharField(max_length=120, blank=True)
    before = models.JSONField(null=True, blank=True)
    after = models.JSONField(null=True, blank=True)
    origen = models.ForeignKey('OrigenInformacion', null=True, blank=True,
                                                    on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"[{self.timestamp}] {self.action} {self.entity}({self.entity_id})"