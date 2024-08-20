# Generated by Django 3.1a1 on 2024-08-19 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0007_auto_20240819_0251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicamento',
            name='via_administración',
            field=models.CharField(choices=[('AU', 'INTRA AURAL'), ('BU', 'BUCAL'), ('CA', 'INTRA CORPUS CAVERNOSUM'), ('CE', 'INTRACEREBRAL'), ('CO', 'CONJUNTIVAL'), ('DE', 'DENTAL'), ('ED', 'EPIDURAL'), ('ES', 'ENDOSINUSAL'), ('HD', 'HEMODIALISIS'), ('HE', 'INTRAHEPATICA'), ('IA', 'INTRA ARTERIAL'), ('IB', 'INTRAVESICAL'), ('IC', 'INTRA CARDIAC'), ('ID', 'INTRADERMAL'), ('IE', 'INTRACAVERNOSA'), ('IF', 'INFILTRATIVA   BLOQUEOS'), ('IG', 'IRRIGACI N'), ('IH', 'INHALACION'), ('II', 'INFUSI N INTRAVENOSA'), ('IK', 'INTRAVASCULAR EN HEMODI LISIS'), ('IL', 'INTRAPLEURAL'), ('IM', 'INTRAMUSCULAR'), ('IN', 'INTRANASAL'), ('IO', 'INTRAOCULAR'), ('IP', 'INTRAPERITONEAL'), ('IR', 'INTRA ARTICULAR'), ('IS', 'INSUFLACION'), ('IT', 'INTRATECAL'), ('IU', 'INTRAUTERINA'), ('IV', 'INTRAVENOSA'), ('IY', 'INFILTRATIVA   LOCAL'), ('IZ', 'INFILTRATIVA   EPIDURAL'), ('LE', 'INTRALESIONAL'), ('LY', 'INTRALINFATICA'), ('MD', 'INTRAMEDULAR  MEDULA DEL HUESO'), ('ME', 'INTRAMENINGEA'), ('MP', 'IMPLANTE'), ('OF', 'OFT LMICA'), ('OT', 'OTICO AURICULAR'), ('PA', 'PERIARTICULAR'), ('PE', 'PERICARDIAL'), ('PI', 'PERFUSION INTRAVENOSA'), ('PN', 'PERINEURAL'), ('PO', 'ORAL'), ('PR', 'RECTAL'), ('PT', 'PARENTERAL'), ('RB', 'RETROBULBAR'), ('RQ', 'RAQUIDEA'), ('SC', 'SUBCUTANEA'), ('SL', 'SUBLINGUAL'), ('SP', 'INTRAESPINAL'), ('SY', 'SISTEMICA  SI LA RUTA NO ES ES'), ('TC', 'T PICA OCULAR'), ('TD', 'TRANSDERMAL'), ('TE', 'TABLETAS CON CUBIERTA ENT RICA'), ('TM', 'TRANSMAMARIA'), ('TO', 'TOPICA  EXTERNA'), ('TP', 'TRANSPLACENTAL'), ('TR', 'INTRATRAQUEAL'), ('UR', 'URETRAL'), ('VA', 'VAGINAL'), ('YL', 'INTRACEREBROVENTRICULAR')], default='PO', max_length=50),
        ),
    ]
