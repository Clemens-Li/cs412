''' Clemens Li | cl750@bu.edu | Views for Intermediate Behavior '''
from django.shortcuts import render
from django.views.generic import ListView, DetailView # Generic Views
from .models import Voter # Models
from django.db.models import Count, Q
import math
import plotly.graph_objs as go
from plotly.offline import plot
# Create your views here.

class VoterListView(ListView):
    ''' Obtains specific data for all Voter objects '''
    model = Voter
    template_name = "voter_analytics/voter_list.html"
    context_object_name = "voters"
    paginate_by = 100 # Show the data for 100 Voters per page

    def get_queryset(self):
        ''' Returns a QuerySet containing all Voter records with an optional conditional filter '''
        qs = super().get_queryset()
        party = self.request.GET.get("party") # Drop-Down
        min_dob = self.request.GET.get("min_dob") # Drop-Down by Year
        max_dob = self.request.GET.get("max_dob") # Drop-Down by Year
        score = self.request.GET.get("score") # Drop-Down
        v20state = self.request.GET.get("v20state") # Checkbox
        v21town = self.request.GET.get("v21town") # Checkbox
        v21primary = self.request.GET.get("v21primary") # Checkbox
        v22general = self.request.GET.get("v22general") # Checkbox
        v23town = self.request.GET.get("v23town") # Checkbox

        # If a variable exists, that specific condition was selected
        if party:
            qs = qs.filter(party=party)
        if min_dob:
            qs = qs.filter(dob__gte=min_dob) # All DOBs after min_dob
        if max_dob:
            qs = qs.filter(dob__lte=max_dob) # All DOBs before max_dob
        if score:
            qs = qs.filter(voter_score=score)
        if v20state:
            qs = qs.filter(v20state=True)
        if v21town:
            qs = qs.filter(v21town=True)
        if v21primary:
            qs = qs.filter(v21primary=True)
        if v22general:
            qs = qs.filter(v22general=True)
        if v23town:
            qs = qs.filter(v23town=True)
        return qs

    def get_context_data(self, **kwargs):
        ''' Returns a context dictionary for use in the template '''
        context = super().get_context_data()
        context["years"] = range(1900, 2027) # Just an estimated range that should encompass all voters?
        context["parties"] = (Voter.objects.exclude(party="").values_list("party", flat=True).distinct().order_by("party")) # Finds all party affiliation codes for template
        return context

class VoterDetailView(DetailView):
    ''' Obtains specific data for a single Voter object '''
    model = Voter
    template_name = "voter_analytics/voter_detail.html"
    context_object_name = "voter"

class GraphListView(ListView):
    ''' Obtains specific data for all Graphs '''
    model = Voter
    template_name = "voter_analytics/graphs.html"

    def get_queryset(self):
        voters = super().get_queryset()
        params = self.request.GET

        if params.get("party"):
            voters = voters.filter(party=params["party"])
        if params.get("min_dob"):
            voters = voters.filter(dob__year__gte=params["min_dob"])
        if params.get("max_dob"):
            voters = voters.filter(dob__year__lte=params["max_dob"])
        if params.get("score"):
            voters = voters.filter(voter_score=params["score"])

        for field in ("v20state", "v21town", "v21primary", "v22general", "v23town"):
            if params.get(field):
                voters = voters.filter(**{field: True})
        return voters

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()
        context["years"] = range(1900, 2027)
        context["parties"] = (
            Voter.objects.exclude(party="")
            .values_list("party", flat=True)
            .distinct()
            .order_by("party")
        )
        birth_years = (
            voters.values("dob__year")
            .annotate(total=Count("id"))
            .order_by("dob__year")
        )
        birth_chart = go.Figure(go.Bar(
            x=[row["dob__year"] for row in birth_years],
            y=[row["total"] for row in birth_years],
        ))
        birth_chart.update_layout(title="Voters by Birth Year", xaxis_title="Year", yaxis_title="Voters")
        party_counts = (
            voters.values("party")
            .annotate(total=Count("id"))
            .order_by("party")
        )
        party_chart = go.Figure(go.Pie(
            labels=[row["party"] or "Unknown" for row in party_counts],
            values=[row["total"] for row in party_counts],
        ))
        party_chart.update_layout(title="Voters by Party")
        elections = (
            ("2020 State", "v20state"),
            ("2021 Town", "v21town"),
            ("2021 Primary", "v21primary"),
            ("2022 General", "v22general"),
            ("2023 Town", "v23town"),
        )
        election_totals = voters.aggregate(**{
            field: Count("id", filter=Q(**{field: True}))
            for _, field in elections
        })
        election_chart = go.Figure(go.Bar(
            x=[label for label, _ in elections],
            y=[election_totals[field] for _, field in elections],
        ))
        election_chart.update_layout(title="Voters by Election Participation", yaxis_title="Voters")
        context["birth_chart"] = plot(birth_chart, output_type="div", include_plotlyjs=False)
        context["party_chart"] = plot(party_chart, output_type="div", include_plotlyjs=False)
        context["election_chart"] = plot(election_chart, output_type="div", include_plotlyjs=False)
        return context
