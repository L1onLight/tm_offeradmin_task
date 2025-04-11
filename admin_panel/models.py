import uuid

from django.db import models, transaction


class OfferChoices(models.TextChoices):
    Loanplus = "Loanplus", "Loanplus"
    SgroshiCPA2 = "SgroshiCPA2", "SgroshiCPA2"
    Novikredyty = "Novikredyty", "Novikredyty"
    TurboGroshi = "TurboGroshi", "TurboGroshi"
    Crypsee = "Crypsee", "Crypsee"
    Suncredit = "Suncredit", "Suncredit"
    Lehko = "Lehko", "Lehko"
    Monto = "Monto", "Monto"
    Limon = "Limon", "Limon"
    Amigo = "Amigo", "Amigo"
    FirstCredit = "FirstCredit", "FirstCredit"
    Finsfera = "Finsfera", "Finsfera"
    Pango = "Pango", "Pango"
    Treba = "Treba", "Treba"
    StarFin = "StarFin", "StarFin"
    BitCapital = "BitCapital", "BitCapital"
    SgroshiCPL = "SgroshiCPL", "SgroshiCPL"
    LoviLave = "LoviLave", "LoviLave"
    Prostocredit = "Prostocredit", "Prostocredit"
    Sloncredit = "Sloncredit", "Sloncredit"
    Clickcredit = "Clickcredit", "Clickcredit"
    Credos = "Credos", "Credos"
    Dodam = "Dodam", "Dodam"
    SelfieCredit = "SelfieCredit", "SelfieCredit"
    Egroshi = "Egroshi", "Egroshi"
    Alexcredit = "Alexcredit", "Alexcredit"
    SgroshiCPA1 = "SgroshiCPA1", "SgroshiCPA1"
    Tengo = "Tengo", "Tengo"
    Credit7 = "Credit7", "Credit7"
    Tpozyka = "Tpozyka", "Tpozyka"
    Creditkasa = "Creditkasa", "Creditkasa"
    Moneyveo = "Moneyveo", "Moneyveo"
    My_Credit = "MyCredit", "MyCredit"
    Credit_Plus = "CreditPlus", "CreditPlus"
    Miloan = "Miloan", "Miloan"
    Avans = "AvansCredit", "AvansCredit"


class OfferWall(models.Model):
    token = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField(null=True, default=None, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"OfferWall {self.token}"

    def add_offer(self, offer, order=None):
        """Add an offer with optional order position"""
        if order is None:
            # If no order specified, put at the end
            max_order = (
                self.offer_assignments.aggregate(models.Max("order"))["order__max"] or 0
            )
            order = max_order + 1
        OfferWallOffer.objects.create(offer_wall=self, offer=offer, order=order)

    def reorder_offers(self, offer_order_list):
        """Reorder offers based on a list of offer UUIDs"""
        with transaction.atomic():
            for index, offer_uuid in enumerate(offer_order_list):
                OfferWallOffer.objects.filter(
                    offer_wall=self, offer__uuid=offer_uuid
                ).update(order=index)

    def get_offers(self):
        """Get all offers in order"""
        return [assignment.offer for assignment in self.offer_assignments.all()]


class Offer(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.IntegerField(primary_key=False)
    url = models.URLField(null=True, default=None, blank=True)
    is_active = models.BooleanField(default=True)

    # Assuming OfferChoices is defined elsewhere
    name = models.CharField(max_length=255, choices=OfferChoices.choices, unique=True)
    sum_to = models.CharField(null=True, default=None, blank=True)
    term_to = models.IntegerField(null=True, default=None, blank=True)
    percent_rate = models.IntegerField(null=True, default=None, blank=True)

    def __str__(self):
        return self.name


class OfferWallOffer(models.Model):
    offer_wall = models.ForeignKey(
        OfferWall, on_delete=models.CASCADE, related_name="offer_assignments"
    )
    offer = models.ForeignKey(
        Offer, on_delete=models.CASCADE, related_name="wall_assignments"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        # unique_together = (
        #     "offer_wall",
        #     "offer",
        # )  # Prevents duplicate offers in same wall
        ordering = ["order"]  # Default ordering by order field

    def __str__(self):
        return f"{self.offer.name} in {self.offer_wall.token} (Order: {self.order})"


class OfferWallPopupOffer(models.Model):
    offer_wall = models.ForeignKey(
        OfferWall, on_delete=models.CASCADE, related_name="popup_assignments"
    )
    offer = models.ForeignKey(
        Offer, on_delete=models.CASCADE, related_name="popup_assignments"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = (
            "offer_wall",
            "offer",
        )  # Prevents duplicate offers in same wall
        ordering = ["order"]  # Default ordering by order field

    def __str__(self):
        return f"{self.offer.name} in {self.offer_wall.token} (Order: {self.order})"
