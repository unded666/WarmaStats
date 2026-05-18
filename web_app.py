import json
from pathlib import Path
from typing import Any, Dict

from flask import Flask, render_template, request

from WM_Analytics import run_wm_analytics

app = Flask(__name__)


FALLBACK_FORM_VALUES: Dict[str, Any] = {
    "defence": 10,
    "attack": 3,
    "power": 5,
    "armour": 2,
    "n_attacks": 1,
    "n_tests": 10000,
    "to_hit_dice": 2,
    "damage_dice": 2,
    "infantry_wounds": "",
}


def _load_default_form_values() -> Dict[str, Any]:
    """Load editable defaults from JSON and merge with fallback keys."""
    defaults_path = Path(__file__).with_name("default_form_values.json")
    try:
        with defaults_path.open("r", encoding="utf-8") as handle:
            loaded_values = json.load(handle)
    except (OSError, json.JSONDecodeError):
        loaded_values = {}

    defaults = dict(FALLBACK_FORM_VALUES)
    if isinstance(loaded_values, dict):
        defaults.update({key: loaded_values.get(key, value) for key, value in FALLBACK_FORM_VALUES.items()})
    return defaults


DEFAULT_FORM_VALUES: Dict[str, Any] = _load_default_form_values()


@app.route("/", methods=["GET", "POST"])
def index():
    """Render the input form and run an experiment when the user submits."""
    form_values = dict(DEFAULT_FORM_VALUES)
    result = None
    error = None

    if request.method == "POST":
        form_values = {
            "defence": request.form.get("defence", "").strip(),
            "attack": request.form.get("attack", "").strip(),
            "power": request.form.get("power", "").strip(),
            "armour": request.form.get("armour", "").strip(),
            "n_attacks": request.form.get("n_attacks", "").strip(),
            "n_tests": request.form.get("n_tests", "").strip(),
            "to_hit_dice": request.form.get("to_hit_dice", "").strip(),
            "damage_dice": request.form.get("damage_dice", "").strip(),
            "infantry_wounds": request.form.get("infantry_wounds", "").strip(),
        }

        try:
            kwargs = {
                "defence": int(form_values["defence"]),
                "attack": int(form_values["attack"]),
                "power": int(form_values["power"]),
                "armour": int(form_values["armour"]),
                "n_attacks": int(form_values["n_attacks"]),
                "n_tests": int(form_values["n_tests"]),
                "to_hit_dice": int(form_values["to_hit_dice"]),
                "damage_dice": int(form_values["damage_dice"]),
            }
            infantry_value = form_values["infantry_wounds"]
            if infantry_value != "":
                kwargs["infantry_wounds"] = int(infantry_value)

            result = run_wm_analytics(**kwargs)
        except ValueError as exc:
            error = f"Invalid input: {exc}"
        except Exception as exc:  # pragma: no cover - keeps UI robust for runtime errors
            error = f"Experiment failed: {exc}"

    return render_template("index.html", form_values=form_values, result=result, error=error)


if __name__ == "__main__":
    app.run(debug=True)

