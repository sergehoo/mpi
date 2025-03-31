from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.

class Landing(TemplateView):
    template_name = "pages/landing.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     today = now().date()
    #     start_of_year = today.replace(month=1, day=1)
    #     start_of_last_year = (today.replace(month=1, day=1, year=today.year - 1))
    #     start_of_month = today.replace(day=1)
    #     start_of_week = today - timedelta(days=today.weekday())
    #
    #     # Filtrage des cas par période
    #     stats_by_period = {
    #         "L'Annee Précédente": {
    #             "postexposition": PostExposition.objects.filter(date_exposition__year=start_of_last_year.year).count(),
    #             "preexposition": Preexposition.objects.filter(created_at__year=start_of_last_year.year).count(),
    #             "notification": RageHumaineNotification.objects.filter(
    #                 date_notification__year=start_of_last_year.year).count(),
    #         },
    #         "Cette Année": {
    #             "postexposition": PostExposition.objects.filter(date_exposition__year=start_of_year.year).count(),
    #             "preexposition": Preexposition.objects.filter(created_at__year=start_of_year.year).count(),
    #             "notification": RageHumaineNotification.objects.filter(
    #                 date_notification__year=start_of_year.year).count(),
    #         },
    #         "Ce mois ci": {
    #             "postexposition": PostExposition.objects.filter(date_exposition__year=today.year,
    #                                                             date_exposition__month=today.month).count(),
    #             "preexposition": Preexposition.objects.filter(created_at__year=today.year,
    #                                                           created_at__month=today.month).count(),
    #             "notification": RageHumaineNotification.objects.filter(date_notification__year=today.year,
    #                                                                    date_notification__month=today.month).count(),
    #         },
    #         "Cette Semaine": {
    #             "postexposition": PostExposition.objects.filter(date_exposition__gte=start_of_week).count(),
    #             "preexposition": Preexposition.objects.filter(created_at__gte=start_of_week).count(),
    #             "notification": RageHumaineNotification.objects.filter(date_notification__gte=start_of_week).count(),
    #         },
    #     }
    #     # Définition des tranches d'âge
    #     age_ranges = {
    #         "0-5 ans": (0, 5),
    #         "6-11 ans": (6, 11),
    #         "12-17 ans": (12, 17),
    #         "18-25 ans": (18, 25),
    #         "26-31 ans": (26, 31),
    #         "32-40 ans": (32, 40),
    #         "41 ans et plus": (41, 150),
    #     }
    #     # Statistiques par tranche d'âge, sexe et type de cas
    #     age_stats = {}
    #     for label, (min_age, max_age) in age_ranges.items():
    #         age_stats[label] = {
    #             "M": {
    #                 "postexposition": PostExposition.objects.filter(
    #                     client__sexe="M",
    #                     client__date_naissance__lte=today - timedelta(days=min_age * 365),
    #                     client__date_naissance__gt=today - timedelta(days=max_age * 365),
    #                 ).count(),
    #                 "preexposition": Preexposition.objects.filter(
    #                     client__sexe="M",
    #                     client__date_naissance__lte=today - timedelta(days=min_age * 365),
    #                     client__date_naissance__gt=today - timedelta(days=max_age * 365),
    #                 ).count(),
    #                 "notification": RageHumaineNotification.objects.filter(
    #                     client__sexe="M",
    #                     client__date_naissance__lte=today - timedelta(days=min_age * 365),
    #                     client__date_naissance__gt=today - timedelta(days=max_age * 365),
    #                 ).count(),
    #             },
    #             "F": {
    #                 "postexposition": PostExposition.objects.filter(
    #                     client__sexe="F",
    #                     client__date_naissance__lte=today - timedelta(days=min_age * 365),
    #                     client__date_naissance__gt=today - timedelta(days=max_age * 365),
    #                 ).count(),
    #                 "preexposition": Preexposition.objects.filter(
    #                     client__sexe="F",
    #                     client__date_naissance__lte=today - timedelta(days=min_age * 365),
    #                     client__date_naissance__gt=today - timedelta(days=max_age * 365),
    #                 ).count(),
    #                 "notification": RageHumaineNotification.objects.filter(
    #                     client__sexe="F",
    #                     client__date_naissance__lte=today - timedelta(days=min_age * 365),
    #                     client__date_naissance__gt=today - timedelta(days=max_age * 365),
    #                 ).count(),
    #             },
    #         }
    #
    #     # Comptage des patients enregistrés ce mois
    #     patients_this_month = {
    #         "postexposition": PostExposition.objects.filter(date_exposition__gte=start_of_month).count(),
    #         "preexposition": Preexposition.objects.filter(created_at__gte=start_of_month).count(),
    #         "notification": RageHumaineNotification.objects.filter(date_notification__gte=start_of_month).count(),
    #     }
    #
    #     # Comptage des patients enregistrés cette semaine
    #     patients_this_week = {
    #         "postexposition": PostExposition.objects.filter(date_exposition__gte=start_of_week).count(),
    #         "preexposition": Preexposition.objects.filter(created_at__gte=start_of_week).count(),
    #         "notification": RageHumaineNotification.objects.filter(date_notification__gte=start_of_week).count(),
    #     }
    #
    #     # Statistiques des motifs de vaccination
    #     motifs = ["voyage", "mise_a_jour", "protection_rage", "chien_voisin", "chiens_errants", "autre"]
    #     context["motif_vaccination_stats"] = {
    #         motif: Preexposition.objects.filter(**{motif: True}).count()
    #         for motif in motifs
    #     }
    #
    #     # Définir les types d'expositions à analyser
    #     exposition_types = [
    #         "morsure",
    #         "griffure",
    #         "lechage_saine",
    #         "lechage_lesee",
    #         "contactanimalpositif",
    #         "contactpatientpositif",
    #         "autre",
    #     ]
    #
    #     # Récupérer les statistiques pour chaque type d'exposition
    #     stats_exposition = {
    #         exposition: PostExposition.objects.filter(**{exposition: True}).count()
    #         for exposition in exposition_types
    #     }
    #
    #     # Ajoutez ces nouvelles données pour les graphiques
    #     # Données mensuelles pour les 12 derniers mois
    #     months = []
    #     postexposition_data = []
    #     preexposition_data = []
    #     notification_data = []
    #
    #     for i in range(11, -1, -1):
    #         month_date = today - relativedelta(months=i)
    #         month_start = month_date.replace(day=1)
    #         month_end = (month_start + relativedelta(months=1)) - timedelta(days=1)
    #
    #         label = month_date.strftime("%b %Y")
    #         months.append(label)
    #
    #         postexposition_data.append({
    #             "x": label,
    #             "y": PostExposition.objects.filter(
    #                 date_exposition__range=(month_start, month_end)
    #             ).count()
    #         })
    #
    #         preexposition_data.append({
    #             "x": label,
    #             "y": Preexposition.objects.filter(
    #                 created_at__range=(month_start, month_end)
    #             ).count()
    #         })
    #
    #         notification_data.append({
    #             "x": label,
    #             "y": RageHumaineNotification.objects.filter(
    #                 date_notification__range=(month_start, month_end)
    #             ).count()
    #         })
    #
    #     context["chart_data"] = {
    #         "months": months,
    #         "postexposition": postexposition_data,
    #         "preexposition": preexposition_data,
    #         "notification": notification_data
    #     }
    #
    #     # Statistiques par niveau géographique
    #     # def get_stats_by_level(model, date_field):
    #     #     stats = {
    #     #         'poles': list(
    #     #             model.objects.values('client__centre_ar__district__region__poles__name')
    #     #             .annotate(count=Count('id'))
    #     #             .order_by('client__centre_ar__district__region__poles__name')
    #     #         ) or [],
    #     #         'regions': list(
    #     #             model.objects.values('client__centre_ar__district__region__name')
    #     #             .annotate(count=Count('id'))
    #     #             .order_by('client__centre_ar__district__region__name')
    #     #         ) or [],
    #     #         'districts': list(
    #     #             model.objects.values('client__centre_ar__district__nom')
    #     #             .annotate(count=Count('id'))
    #     #             .order_by('client__centre_ar__district__nom')
    #     #         ) or [],
    #     #         'centres': list(
    #     #             model.objects.values('client__centre_ar__nom')
    #     #             .annotate(count=Count('id'))
    #     #             .order_by('client__centre_ar__nom')
    #     #         ) or []
    #     #     }
    #     #     return stats
    #     #
    #     # context['stats_geo'] = {
    #     #     'preexposition': get_stats_by_level(Preexposition, 'created_at'),
    #     #     'postexposition': get_stats_by_level(PostExposition, 'date_exposition'),
    #     #     'notification': get_stats_by_level(RageHumaineNotification, 'date_notification')
    #     # }
    #     #
    #     # # Statistiques détaillées par centre
    #     # centres = CentreAntirabique.objects.all()
    #     # centre_stats = []
    #     # for centre in centres:
    #     #     district_name = centre.district.nom if centre.district else "N/A"
    #     #
    #     #     stats = {
    #     #
    #     #         'centre': centre.nom,
    #     #         'district': centre.district.nom if centre.district else '',
    #     #         'region': centre.district.region.name if centre.district and centre.district.region else '',
    #     #         'pole': centre.district.region.poles.name if centre.district and centre.district.region and centre.district.region.poles else '',
    #     #         'preexposition': Preexposition.objects.filter(client__centre_ar=centre).count(),
    #     #         'postexposition': PostExposition.objects.filter(client__centre_ar=centre).count(),
    #     #         'notification': RageHumaineNotification.objects.filter(client__centre_ar=centre).count(),
    #     #         'total': Preexposition.objects.filter(client__centre_ar=centre).count() +
    #     #                  PostExposition.objects.filter(client__centre_ar=centre).count() +
    #     #                  RageHumaineNotification.objects.filter(client__centre_ar=centre).count()
    #     #     }
    #     #     centre_stats.append(stats)
    #     #
    #     #
    #     # context['centre_stats'] = sorted(centre_stats, key=lambda x: x['total'], reverse=True)
    #
    #     # context["stats_exposition"] = stats_exposition
    #     # debut stat par centre
    #     centres = CentreAntirabique.objects.annotate(
    #         total_preexposition=Count('patient__preexposition', distinct=True),
    #         total_postexposition=Count('patient__postexposition', distinct=True),
    #         total_notifications=Count('patient__notifications_rage', distinct=True),
    #         total_vaccinations=Count('patient__vaccination', distinct=True),
    #         total_mapis=Count('patient__mapi', distinct=True),
    #     ).select_related('district__region__poles').order_by('-total_preexposition', '-total_postexposition',
    #                                                          '-total_vaccinations', '-total_mapis')
    #
    #     context["centres"] = centres
    #     # fin stat par centre
    #     # debut stat par  districts
    #     districts = DistrictSanitaire.objects.annotate(
    #         total_preexposition=Count('centres__patient__preexposition', distinct=True),
    #         total_postexposition=Count('centres__patient__postexposition', distinct=True),
    #         total_notifications=Count('centres__patient__notifications_rage', distinct=True),
    #         total_vaccinations=Count('centres__patient__vaccination', distinct=True),
    #         total_mapis=Count('centres__patient__mapi', distinct=True),
    #     ).select_related('region__poles').order_by('-total_preexposition', '-total_postexposition',
    #                                                '-total_vaccinations', '-total_mapis')
    #     context["district"] = districts
    #     # fin stat par district
    #     # debut stat par  regions
    #     regions = HealthRegion.objects.annotate(
    #         total_preexposition=Count('districts__centres__patient__preexposition', distinct=True),
    #         total_postexposition=Count('districts__centres__patient__postexposition', distinct=True),
    #         total_notifications=Count('districts__centres__patient__notifications_rage', distinct=True),
    #         total_vaccinations=Count('districts__centres__patient__vaccination', distinct=True),
    #         total_mapis=Count('districts__centres__patient__mapi', distinct=True),
    #     ).select_related('poles').order_by('-total_preexposition', '-total_postexposition', '-total_vaccinations',
    #                                        '-total_mapis')
    #
    #     context["statts_regions"] = regions
    #     # fin stat par centre
    #
    #     # debut stat par  pres
    #     poles = PolesRegionaux.objects.annotate(
    #         total_preexposition=Count('regions__districts__centres__patient__preexposition', distinct=True),
    #         total_postexposition=Count('regions__districts__centres__patient__postexposition', distinct=True),
    #         total_notifications=Count('regions__districts__centres__patient__notifications_rage', distinct=True),
    #         total_vaccinations=Count('regions__districts__centres__patient__vaccination', distinct=True),
    #         total_mapis=Count('regions__districts__centres__patient__mapi', distinct=True),
    #     ).order_by('-total_preexposition', '-total_postexposition', '-total_vaccinations', '-total_mapis')
    #     context["stats_poles"] = poles
    #     # fin stat par centre
    #
    #     context["patients_this_month"] = patients_this_month
    #     context["patients_this_week"] = patients_this_week
    #
    #     context["stats_by_period"] = stats_by_period
    #     context["age_stats"] = age_stats
    #     context["patients_geojson_url"] = "/patients_geojson/"
    #     return context