from django.db.models import Q, Sum

from .models import Displacement


def get_displacement_stats(queryset=None):
    """
    Computes and returns summary analytics for displacement data.
    """
    if queryset is None:
        queryset = Displacement.objects.all()

    stats = queryset.aggregate(
        total_male=Sum("males_number"),
        total_female=Sum("female_number"),
        total_vulnerable_hhs=Sum("total_vul_hhs"),
        males_0_4=Sum("males_number_0_4"),
        females_0_4=Sum("females_number_0_4"),
        males_5_17=Sum("males_number_5_17"),
        females_5_17=Sum("females_number_5_17"),
        males_18_59=Sum("males_number_18_59"),
        females_18_59=Sum("females_number_18_59"),
        males_60_plus=Sum("males_number_60_plus"),
        females_60_plus=Sum("females_number_60_plus"),
    )

    total_male = stats["total_male"] or 0
    total_female = stats["total_female"] or 0
    total_idp = total_male + total_female

    total_vulnerable_hhs = stats["total_vulnerable_hhs"] or 0
    total_0_4 = (stats["males_0_4"] or 0) + (stats["females_0_4"] or 0)
    total_5_17 = (stats["males_5_17"] or 0) + (stats["females_5_17"] or 0)
    total_18_59 = (stats["males_18_59"] or 0) + (stats["females_18_59"] or 0)
    total_60_plus = (stats["males_60_plus"] or 0) + (stats["females_60_plus"] or 0)

    # Unique operations count
    operation_count = queryset.values("operation").distinct().count()

    # Breakdown by reporting year
    year_stats = (
        queryset
        .exclude(reporting_year__isnull=True)
        .values("reporting_year")
        .annotate(
            total_male=Sum("males_number"),
            total_female=Sum("female_number"),
            total_vulnerable_hhs=Sum("total_vul_hhs"),
            males_0_4=Sum("males_number_0_4"),
            females_0_4=Sum("females_number_0_4"),
            males_5_17=Sum("males_number_5_17"),
            females_5_17=Sum("females_number_5_17"),
            males_18_59=Sum("males_number_18_59"),
            females_18_59=Sum("females_number_18_59"),
            males_60_plus=Sum("males_number_60_plus"),
            females_60_plus=Sum("females_number_60_plus"),
        )
        .order_by("reporting_year")
    )

    idps_by_year = []
    for item in year_stats:
        y = item["reporting_year"]
        m = item["total_male"] or 0
        f = item["total_female"] or 0
        v_hhs = item["total_vulnerable_hhs"] or 0
        age_0_4 = (item["males_0_4"] or 0) + (item["females_0_4"] or 0)
        age_5_17 = (item["males_5_17"] or 0) + (item["females_5_17"] or 0)
        age_18_59 = (item["males_18_59"] or 0) + (item["females_18_59"] or 0)
        age_60_plus = (item["males_60_plus"] or 0) + (item["females_60_plus"] or 0)
        idps_by_year.append({
            "year": y,
            "total_male": m,
            "total_female": f,
            "total_idp": m + f,
            "total_vulnerable_hhs": v_hhs,
            "total_0_4": age_0_4,
            "total_5_17": age_5_17,
            "total_18_59": age_18_59,
            "total_60_plus": age_60_plus,
        })

    # Breakdown by admin1_name
    admin1_stats = (
        queryset
        .exclude(Q(admin1_name__isnull=True) | Q(admin1_name=""))
        .values("admin1_name")
        .annotate(
            total_male=Sum("males_number"),
            total_female=Sum("female_number"),
            total_vulnerable_hhs=Sum("total_vul_hhs"),
            males_0_4=Sum("males_number_0_4"),
            females_0_4=Sum("females_number_0_4"),
            males_5_17=Sum("males_number_5_17"),
            females_5_17=Sum("females_number_5_17"),
            males_18_59=Sum("males_number_18_59"),
            females_18_59=Sum("females_number_18_59"),
            males_60_plus=Sum("males_number_60_plus"),
            females_60_plus=Sum("females_number_60_plus"),
        )
        .order_by("admin1_name")
    )

    admin1_map = {}
    for item in admin1_stats:
        adm = item["admin1_name"]
        if not adm or not adm.strip():
            continue
        adm_name = adm.strip()
        if adm_name not in admin1_map:
            admin1_map[adm_name] = {
                "admin1_name": adm_name,
                "total_male": 0,
                "total_female": 0,
                "total_idp": 0,
                "total_vulnerable_hhs": 0,
                "total_0_4": 0,
                "total_5_17": 0,
                "total_18_59": 0,
                "total_60_plus": 0,
            }
        m = item["total_male"] or 0
        f = item["total_female"] or 0
        v_hhs = item["total_vulnerable_hhs"] or 0
        age_0_4 = (item["males_0_4"] or 0) + (item["females_0_4"] or 0)
        age_5_17 = (item["males_5_17"] or 0) + (item["females_5_17"] or 0)
        age_18_59 = (item["males_18_59"] or 0) + (item["females_18_59"] or 0)
        age_60_plus = (item["males_60_plus"] or 0) + (item["females_60_plus"] or 0)
        admin1_map[adm_name]["total_male"] += m
        admin1_map[adm_name]["total_female"] += f
        admin1_map[adm_name]["total_idp"] += m + f
        admin1_map[adm_name]["total_vulnerable_hhs"] += v_hhs
        admin1_map[adm_name]["total_0_4"] += age_0_4
        admin1_map[adm_name]["total_5_17"] += age_5_17
        admin1_map[adm_name]["total_18_59"] += age_18_59
        admin1_map[adm_name]["total_60_plus"] += age_60_plus

    idps_by_admin1 = list(admin1_map.values())

    return {
        "total_idp": total_idp,
        "total_male": total_male,
        "total_female": total_female,
        "total_vulnerable_hhs": total_vulnerable_hhs,
        "total_0_4": total_0_4,
        "total_5_17": total_5_17,
        "total_18_59": total_18_59,
        "total_60_plus": total_60_plus,
        "operation_count": operation_count,
        "idps_by_year": idps_by_year,
        "idps_by_admin1": idps_by_admin1,
    }


def get_displacement_unique_filters():
    """
    Returns unique values for admin1_name, operation, and reporting_year.
    """
    base_qs = Displacement.objects.filter(status=Displacement.StatusChoices.VERIFIED)
    admin1_names = (
        base_qs
        .exclude(admin1_name__isnull=True)
        .exclude(admin1_name="")
        .values_list("admin1_name", flat=True)
        .distinct()
        .order_by("admin1_name")
    )
    operations = (
        base_qs
        .exclude(operation__isnull=True)
        .exclude(operation="")
        .values_list("operation", flat=True)
        .distinct()
        .order_by("operation")
    )
    reporting_years = (
        base_qs
        .exclude(reporting_year__isnull=True)
        .values_list("reporting_year", flat=True)
        .distinct()
        .order_by("reporting_year")
    )

    # Strip whitespace from names/operations to ensure uniqueness
    unique_admin1 = sorted(
        list(set(name.strip() for name in admin1_names if name and name.strip()))
    )
    unique_operations = sorted(
        list(set(op.strip() for op in operations if op and op.strip()))
    )
    unique_years = sorted(list(reporting_years))

    return {
        "admin1_names": unique_admin1,
        "operations": unique_operations,
        "reporting_years": unique_years,
    }
