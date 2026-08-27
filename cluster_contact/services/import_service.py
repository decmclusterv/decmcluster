import io
import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from django.conf import settings

from cluster_contact.models import ClusterContact

FREE_EMAIL_PROVIDERS = {
    "gmail",
    "yahoo",
    "hotmail",
    "outlook",
    "aol",
    "icloud",
    "mail.gmail",
}


def extract_organization_from_email(email: str) -> Optional[str]:
    """
    Extracts organization name based on domain part of email.
    If email domain is a free provider like gmail, returns None.
    Examples:
        - sbenjimen@unicef.org -> UNICEF
        - alex@wfp.org -> WFP
        - user@gmail.com -> None
    """
    if not email or "@" not in email:
        return None

    domain = email.split("@")[-1].lower()

    if any(provider in domain for provider in FREE_EMAIL_PROVIDERS):
        return None

    parts = domain.split(".")
    if not parts or not parts[0]:
        return None

    org = parts[0]

    known_orgs = {
        "unicef": "UNICEF",
        "undp": "UNDP",
        "un": "UN",
        "wfp": "WFP",
        "fao": "FAO",
        "who": "WHO",
        "iom": "IOM",
        "dfat": "DFAT",
        "mfat": "MFAT",
        "jica": "JICA",
        "usaid": "USAID",
        "adra": "ADRA",
        "wvi": "WVI",
        "unwomen": "UN Women",
        "ifrc": "IFRC",
        "adb": "ADB",
        "afd": "AFD",
    }

    if org.lower() in known_orgs:
        return known_orgs[org.lower()]

    return org.upper() if len(org) <= 4 else org.capitalize()


def parse_contacts_from_docx(
    file_source: Union[str, Path, bytes, io.BytesIO]
) -> List[Tuple[str, str, Optional[str]]]:
    """
    Parses name, email, and organization from a docx file stream or file path.
    """
    if isinstance(file_source, (str, Path)):
        z = zipfile.ZipFile(file_source)
    else:
        if isinstance(file_source, bytes):
            file_source = io.BytesIO(file_source)
        z = zipfile.ZipFile(file_source)

    with z:
        xml_content = z.read("word/document.xml")
        tree = ET.fromstring(xml_content)
        texts = [elem.text for elem in tree.iter() if elem.text]
        full_text = " ".join(texts)

    pattern = (
        r'(?:[\"\']?([^<>\n\r,]+?)[\"\']?\s*)?<([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})>|'
        r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"
    )
    raw_entries = re.findall(pattern, full_text)

    contacts = []
    seen_emails = set()

    for match in raw_entries:
        raw_name, email_in_angle, standalone_email = match
        email = (email_in_angle or standalone_email).strip().lower()
        if not email or email in seen_emails:
            continue
        seen_emails.add(email)

        name = raw_name.strip() if raw_name else ""
        name = re.sub(r"^[,\s\"\'\xa0]+|[,\s\"\'\xa0]+$", "", name)

        if not name:
            prefix = email.split("@")[0]
            name = prefix.replace(".", " ").replace("_", " ").replace("-", " ").title()

        org = extract_organization_from_email(email)
        contacts.append((name, email, org))

    return contacts


def import_contacts_from_docx_file(
    file_source: Optional[Union[str, Path, bytes, io.BytesIO]] = None
) -> Dict[str, Any]:
    """
    Imports contacts into ClusterContact model from a docx file.
    Defaults to 'DECM Cluster Mailing List.docx' in BASE_DIR if file_source is None.
    """
    if file_source is None:
        file_source = Path(settings.BASE_DIR) / "DECM Cluster Mailing List.docx"

    parsed_contacts = parse_contacts_from_docx(file_source)

    created_count = 0
    updated_count = 0

    for name, email, organization in parsed_contacts:
        _, created = ClusterContact.objects.update_or_create(
            email=email,
            defaults={
                "name": name,
                "organization": organization,
            },
        )
        if created:
            created_count += 1
        else:
            updated_count += 1

    return {
        "created_count": created_count,
        "updated_count": updated_count,
        "total_processed": len(parsed_contacts),
    }
