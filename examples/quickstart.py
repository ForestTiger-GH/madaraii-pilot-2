from cbr_unified import UnifiedDatabase


db = UnifiedDatabase("./build/cbr/data/cbr_unified.sqlite")

# Find source-local statistical concepts using the Russian source-facing surface.
print(db.indicators("ипотеч", language="ru").head(20))

# Long-form observations suitable for pandas analysis.
observations = db.observations(
    source_ids="mortgage_debt",
    start="2025-01-01",
    end="2026-08-01",
    dimensions={"currency_category": "rubles"},
    language="ru",
)
print(observations.head())

# A deliberately explicit slice can be pivoted without implicit aggregation.
wide = db.pivot(
    source_ids="mortgage_debt",
    start="2025-01-01",
    end="2026-08-01",
    dimensions={
        "currency_category": "rubles",
        "region": "РОССИЙСКАЯ ФЕДЕРАЦИЯ",
    },
    index="period",
    columns="indicator",
    language="ru",
)
print(wide)

# Exact source evidence for any analytical observation.
if not observations.empty:
    print(db.lineage(str(observations.iloc[0]["observation_id"])))
