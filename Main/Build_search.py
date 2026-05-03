from Backend.Build import Build
from Backend.Item import Item
from Backend.Database import Database
from Backend.GeneticAlgorithm import GeneticAlgorithm
from pandas import DataFrame

#import matplotlib.pyplot as plt
import streamlit as st


def evaluate_tankiness_index(item: Item):
    return item.get_combination([
            # find from json 
            ['base', 'baseHealth'], 
            ['identifications', 'rawHealth'],
            ['identifications', 'healthRegenRaw'],
            ['identifications', 'healthRegen'],
            ['identifications', 'rawDefence'],
            ['identifications', 'rawAgility'],
            ['identifications', 'walkSpeed'],
            ['identifications', 'rawMainAttackDamage'],
            ['identifications', 'rawSpellDamage'],
            ['identifications', 'poison']
            ],
            { 
            # add weights for stats
            "baseHealth":4.25,
            "rawHealth":3.25,
            "healthRegen": 100.35, # a lot higher since the distribution of health regen % is lot lower than raw
            "healthRegenRaw":35.45,
            "rawDefence":70,
            "rawAgility":70,
            "walkSpeed":32,
            "rawMainAttackDamage":1,
            "rawSpellDamage":1,
            "poison":0.1
            })


def evaluate_index_dummy(item: Item):
    return 0

def generate_index(names, weights):
    def evaluate_index(item: Item):
        return item.get_combination(
            names,
            weights
        )
    return evaluate_index

def evaluate_builds(weapon, index, iterations, population_size = 1000):
    items = Database(index, weapon)
    print(items.get_accessory_table())
    ga = GeneticAlgorithm(items, 1000)
    x, yBest, yAverage = ga.generations(iterations)
    ga.sort_population()
    best_individual = ga.get_population()[0]
    return best_individual, x, yBest, yAverage, items


def streamlit_main():
    st.set_page_config(
        "Wynncraft Build Solver",
        layout="wide"
    )

    main_container = st.container(horizontal=True, horizontal_alignment="left")
    generator_details = main_container.container()

    generator_details.title("**:green[Wynncraft] Build Solver**")
    generator_details.markdown(
        """ 
        *A local only tool for build solving!* The only tool you will need!
        """
    )

    if "data" not in st.session_state:
        st.session_state.data = Database(evaluate_index_dummy, "spear")
    
    data = st.session_state.data
    stat_list = data.get_stat_list()

    iterations = generator_details.number_input("Choose iteration amount", 0, width=200)
    weapon = generator_details.selectbox("Choose weapon", options=data.get_weapon_table(), key="weapon_box", width=250)
    inputs = generator_details.container(border=True, width=1000)
    inputs_horizontal = inputs.container(horizontal=True, width=1000)
    main_statistic_user_input = inputs_horizontal.selectbox("Choose statistic", index=None, placeholder="Select a statistic", options=stat_list, key="statistic_box", width=400)
    main_statistic_user_input_weight = inputs_horizontal.number_input("Weight", key="statistic_weight", width=200)

    weight_list = generator_details.container(border=True, width=1000, height=500)

    if "rows" not in st.session_state:
        st.session_state.rows = {}

    if "next_id" not in st.session_state:
        st.session_state.next_id = 0
    
    if inputs.button("Add", width=100):
        if main_statistic_user_input is not None:
            rid = st.session_state.next_id
            st.session_state.next_id += 1

            st.session_state.rows[rid] = {
                "stat": main_statistic_user_input,
                "weight": main_statistic_user_input_weight
            }

    to_delete = []
    for rid, row in st.session_state.rows.items():
        container = weight_list.container(
            horizontal=True,
            border=True,
            vertical_alignment="center"
        )

        stat = container.selectbox(
            "Statistic",
            options=stat_list,
            index=stat_list.index(row["stat"]),
            key=f"stat_{rid}"
        )

        weight = container.number_input(
            "Weight",
            value=row["weight"],
            key=f"weight_{rid}"
        )

        # sync edits back to state
        st.session_state.rows[rid]["stat"] = stat
        st.session_state.rows[rid]["weight"] = weight

        if container.button("Remove", key=f"del_{rid}"):
            to_delete.append(rid)

    if generator_details.button("Generate", width=1000):
        collected_index_calculation = []
        collected_weight_calculation = {}
        inverse_stat_table = data.get_inverse_stat_table()
        for rid, row in st.session_state.rows.items():
            collected_index_calculation.append([inverse_stat_table[row['stat']], row['stat']])
            collected_weight_calculation[row['stat']] = row['weight']

        with st.spinner("Generating..."):
            bestBuild, x, yBest, yAverage, newItems = evaluate_builds(
                weapon,
                generate_index(collected_index_calculation, collected_weight_calculation),
                iterations
            )


        st.success("Completed!")

        st.session_state.data = newItems

        result_container = main_container.container(
            horizontal=False,
            border=True,
            vertical_alignment="top",
            height=1000,
            horizontal_alignment="left"
        )

        result_container.markdown("**Result**")

        step_size = max(int(len(x) * 0.1), 1)

        x = x[0:-1:step_size]

        dataframe = DataFrame({"yBest" : yBest[0:-1:step_size], "yAverage" : yAverage[0:-1:step_size]}, index=x)

        result_container.line_chart(dataframe)
        build_items = bestBuild.get_items()
        for key in build_items:
            result_container.text("%s: %s"%(key, build_items[key]))

    if to_delete:
        for rid in to_delete:
            del st.session_state.rows[rid]
        st.rerun()

    return 0
                                            

# Main
if __name__ == '__main__':
    #main()
    streamlit_main()

