import os 
import matplotlib.pyplot as plt
import json

Data = {}

def load_data(folder: str) -> dict[str, dict]:
    alldata = {}
    for year in [item.name for item in os.scandir(folder) if os.path.isdir(item)]:
        for subject in [item.name for item in os.scandir(os.path.join(folder, year)) if str.endswith(item.name, ".json")]:
            subjname = str.replace(subject, ".json", "")
            yeardata = alldata.get(year, {})
            try:
                with open(os.path.join(folder, year, subject), "r", encoding="utf-8") as f:
                    data = json.load(f)
                    yeardata[subjname] = data
                    alldata[year] = yeardata

            except FileNotFoundError:
                pass
            except json.JSONDecodeError:
                pass
    return alldata


def result_plot(subject: str, year: int):
    try:
        statdata : dict = Data[str(year)][subject]
        stats = {}
        for _, grade in statdata.items():
            count = stats.get(grade, 0) + 1
            stats[grade] = count
        
        plt.bar(stats.keys(), stats.values())
        plt.xlabel("Érdemjegy")
        plt.ylabel("Darab")
        plt.title(f"Eloszlás {year} {subject}")
        plt.tight_layout(pad=2)
        plt.savefig(f"{subject}_{year}_results.png")
    
    except KeyError as err:
        print(err)


def result_plot_over_years(subjects: list):
    stats = {}
    for subject in subjects:
        years = Data.keys()
        stats = {}
        for year in years:
            yeardata = Data.get(year, {})
            subjdata: dict  = yeardata.get(subject, {})
            passed = len([grade for _, grade in subjdata.items() if grade > 1])
            stats[year] = round(passed / len(subjdata)*100) if len(subjdata) > 0 else 0
        plt.plot(stats.keys(), stats.values(), label=subject)
    
    plt.title(f"{', '.join(subjects)} átmeneti grafikon")
    plt.xlabel("Év")
    plt.ylabel("Átment %")
    plt.legend()
    plt.tight_layout(pad=2)
    plt.show()

def main():
    global Data 
    Data = load_data('results')
    result_plot("math", 2020)
    result_plot_over_years(['art', 'math', 'music'])

main()

