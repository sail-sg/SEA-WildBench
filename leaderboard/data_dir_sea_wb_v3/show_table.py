import json
import re

import fire
from tabulate import tabulate


def flatten_dict(d, parent_key='', sep='.'):
    flattened = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            flattened.update(flatten_dict(v, new_key, sep=sep))
        else:
            flattened[new_key] = v
    return flattened

def show_table(K=-1, mode="taskwise_reward", bench_name='sea', normalized_reward=True, filter_pattern=None):
    """
    Args: 
        bench_name: str, "sea" for sea-wildbench, "wb" for wildbench
    """

    if bench_name == "sea-mini":
        main_file = f"leaderboard/data_dir_sea_wb_v3/pairsea-4o-mini-4o-K={K}.json"
    # elif bench_name == "wb":
    #     main_file = f"leaderboard/data_dir_sea_wb_v3/pairwise-qwen-K={K}.json"
    elif bench_name == "sea-4o":
        main_file = f"leaderboard/data_dir_sea_wb_v3/pairsea-4o-4o-K={K}.json"
    # elif bench_name == "wb-4o":
    #     main_file = f"leaderboard/data_dir_sea_wb_v3/pairwise-qwen-4o-K={K}.json"
    else:
        raise ValueError("bench_name should be either 'sea-mini' or 'sea-4o'")
    with open(main_file, "r") as f:
        all_stat = json.load(f)
        all_stat = {k: flatten_dict(v) for k, v in all_stat.items()}

    # -------- original implementation --------
    # all_column_names = ['Arena Elo (hard) - 2024-05-20', 'Arena-Hard v0.1', 'AE2.0 LC', 'AE2.0', 'Arena Elo (hard-en) - 2024-06-06', 'haiku_reward.K=$K', 'llama_reward.K=$K', 'gpt4t_reward.K=$K', 'haiku_reward.Creative Tasks.K=$K', 'llama_reward.Creative Tasks.K=$K', 'gpt4t_reward.Creative Tasks.K=$K', 'mixture_of_rewards.Creative Tasks.K=$K', 'haiku_reward.Planning & Reasoning.K=$K', 'llama_reward.Planning & Reasoning.K=$K', 'gpt4t_reward.Planning & Reasoning.K=$K', 'mixture_of_rewards.Planning & Reasoning.K=$K', 'haiku_reward.Math & Data Analysis.K=$K', 'llama_reward.Math & Data Analysis.K=$K', 'gpt4t_reward.Math & Data Analysis.K=$K', 'mixture_of_rewards.Math & Data Analysis.K=$K', 'haiku_reward.Information/Advice seeking.K=$K', 'llama_reward.Information/Advice seeking.K=$K', 'gpt4t_reward.Information/Advice seeking.K=$K', 'mixture_of_rewards.Information/Advice seeking.K=$K', 'haiku_reward.Coding & Debugging.K=$K', 'llama_reward.Coding & Debugging.K=$K', 'gpt4t_reward.Coding & Debugging.K=$K', 'mixture_of_rewards.Coding & Debugging.K=$K', 'haiku_reward.task_macro.K=$K', 'llama_reward.task_macro.K=$K', 'gpt4t_reward.task_macro.K=$K', 'mixture_of_rewards.K=$K', 'task_macro_reward.K=$K', 'WB_score.Creative Tasks', 'WB_score.Planning & Reasoning', 'WB_score.Math & Data Analysis', 'WB_score.Information/Advice seeking', 'WB_score.Coding & Debugging', 'WB_score', 'WB_score.task_macro', 'Length', 'Rank_ScoreMacro', 'Rank_TaskMacroReward.K', 'Rank_Avg', 'RewardScore_Avg', 'WB_Elo']
    # all_column_names = [x.replace("$K", str(K)) for x in all_column_names]

    # if mode == "main":
    #     all_column_names_to_show = ["WB_Elo", "RewardScore_Avg", "WB_score.task_macro", f"task_macro_reward.K={K}", "Length"] 
    #     rank_column = "WB_Elo"
    # elif mode == "taskwise_score":
    #     all_column_names_to_show = ["WB_Elo", "WB_score.task_macro", "WB_score.Creative Tasks", "WB_score.Planning & Reasoning", "WB_score.Math & Data Analysis", "WB_score.Information/Advice seeking", "WB_score.Coding & Debugging", "Length"]
    #     # rank_column = "WB_score.task_macro"
    #     rank_column = "WB_Elo"
    # elif mode == "taskwise_reward":
    #     all_column_names_to_show = ["WB_Elo", f"task_macro_reward.K={K}", f"mixture_of_rewards.Creative Tasks.K={K}", f"mixture_of_rewards.Planning & Reasoning.K={K}", f"mixture_of_rewards.Math & Data Analysis.K={K}", f"mixture_of_rewards.Information/Advice seeking.K={K}", f"mixture_of_rewards.Coding & Debugging.K={K}", "Length"]
    #     rank_column = f"task_macro_reward.K={K}"
    # else:
    #     raise NotImplementedError
    # -------- original implementation --------

    if mode == "taskwise_reward":
        all_column_names_to_show = [
            "task_macro_reward", "reward", "task_categorized_rewards.Coding & Debugging", "task_categorized_rewards.Creative Tasks", "task_categorized_rewards.Information/Advice seeking", "task_categorized_rewards.Planning & Reasoning", "task_categorized_rewards.Math & Data Analysis", "total", "avg_len", 
        ]
        all_column_names_to_show_formatted = [
            "Task Weighted Reward", "Reward", "Coding & Debugging", "Creative Tasks", "Information/Advice seeking", "Planning & Reasoning", "Math & Data Analysis", "Total", "Avg. Length",
        ]
        rank_column = "task_macro_reward"

        if normalized_reward: 
            all_column_names_to_show = [ f"{c}.normalized" if "reward" in c else c for c in all_column_names_to_show]
            rank_column = "task_macro_reward.normalized"
    elif mode == "lanwise_reward":
        all_column_names_to_show = [
            "reward", "lan_categorized_rewards.tha_Thai", "lan_categorized_rewards.vie_Latn", "lan_categorized_rewards.ind_Latn", "lan_categorized_rewards.tgl_Latn", "lan_categorized_rewards.zsm_Latn", "lan_categorized_rewards.khm_Khmr", "lan_categorized_rewards.lao_Laoo", "lan_categorized_rewards.mya_Mymr", "task_macro_reward", "total", "avg_len", 
        ]
        all_column_names_to_show_formatted = [
            "Reward", "tha", "vie", "ind", "tgl", "zsm", "khm", "lao", "mya", "Task Weighted Reward", "Total", "Avg. Length",
        ]
        rank_column = "reward"
        
        if normalized_reward: 
            all_column_names_to_show = [ f"{c}.normalized" if "reward" in c else c for c in all_column_names_to_show]
            rank_column = "reward.normalized"
    else:
        raise NotImplementedError
    
    # rank by rank_column   
    print(f"Ranking by {rank_column}")
    all_stat = {k: v for k, v in sorted(all_stat.items(), key=lambda item: item[1][rank_column], reverse=True)}
     
    if filter_pattern is not None:
        all_stat = {k: v for k, v in all_stat.items() if re.match(filter_pattern, k)}

    rows = []
    for item in all_stat:
        row = [item] + [all_stat[item][x] for x in all_column_names_to_show]
        rows.append(row)
    
    # show a table for the local leaderboard
    # add a rank column 
    print(tabulate(rows, headers=["Model"] + all_column_names_to_show_formatted, tablefmt="github", showindex="always", floatfmt=".2f"))


# main 
if __name__ == "__main__":
    fire.Fire(show_table)