from django.conf import settings

from decmcluster.services.email_service import send_model_verification_email


def send_displacement_import_verification_email(instance, comment=None):
    """
    Utility function to send a verification request email for a DisplacementImport instance to the admin.
    """
    file_url = instance.file.url if instance.file else None
    uploader_name = (
        f"{instance.uploaded_by.first_name} {instance.uploaded_by.last_name}".strip()
        or instance.uploaded_by.email
        if instance.uploaded_by
        else "Anonymous"
    )
    details = [
        {"label": "Import ID", "value": str(instance.id)},
        {"label": "Name", "value": instance.name or "N/A"},
        {
            "label": "File Name",
            "value": instance.file.name.split("/")[-1] if instance.file else "N/A",
        },
        {"label": "Status", "value": instance.status.capitalize()},
        {"label": "Uploaded By", "value": uploader_name},
    ]
    if file_url:
        details.append({"label": "File", "value": file_url, "is_link": True})
    if comment:
        details.append({"label": "Uploader Comment", "value": comment})

    base_url = getattr(settings, "ADMIN_URL", "http://192.168.1.80:3000/")
    if not base_url.endswith("/"):
        base_url += "/"
    admin_url = f"{base_url}displacement-imports/verify/{instance.id}/"
    print("admin_url", admin_url)

    return send_model_verification_email(
        instance=instance,
        model_name="Displacement Import",
        details=details,
        admin_url=admin_url,
    )


def send_displacement_verification_email(instance, comment=None):
    """
    Utility function to send a verification request email for a Displacement instance to the admin.
    """
    uploader_name = (
        f"{instance.uploaded_by.first_name} {instance.uploaded_by.last_name}".strip()
        or instance.uploaded_by.email
        if instance.uploaded_by
        else "Anonymous"
    )
    details = [
        {"label": "Operation", "value": instance.operation},
        {"label": "Reporting Date", "value": str(instance.reporting_date) if instance.reporting_date else "N/A"},
        {"label": "Admin 1", "value": instance.admin1_name or "N/A"},
        {"label": "IDPs Count", "value": str(instance.num_present_idps) if instance.num_present_idps is not None else "N/A"},
        {"label": "Status", "value": instance.status.capitalize()},
        {"label": "Uploaded By", "value": uploader_name},
    ]
    if comment:
        details.append({"label": "Uploader Comment", "value": comment})

    base_url = getattr(settings, "ADMIN_URL", "http://192.168.1.80:3000/")
    if not base_url.endswith("/"):
        base_url += "/"
    admin_url = f"{base_url}displacements/verify/{instance.id}/"
    print("admin_url", admin_url)

    return send_model_verification_email(
        instance=instance,
        model_name="Displacement",
        details=details,
        admin_url=admin_url,
    )
