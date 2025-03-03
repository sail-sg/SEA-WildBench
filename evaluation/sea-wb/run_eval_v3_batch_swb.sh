model_name=$1 # model to test 
# by default use gpt-4o-2024-08-06 as ref_name
ref_name=${2:-"gpt-4o-2024-08-06"} # model to compare 
# by default use "gpt-4o-2024-08-06" as gpt_eval_name
gpt_eval_name=${3:-"gpt-4o-2024-08-06"} # evaluator name
# by default use "sea" as eval_config
eval_config=${4:-"sea"} # evaluation config, wb or wbc (custom), or sea


eval_template="evaluation/sea-wb/eval_template.pairwise.v3.md"
echo "Evaluating $model_name vs $ref_name using $gpt_eval_name with $eval_template with $eval_config"


if [ $eval_config == "wb" ]; then
    export HF_BENCH_PATH=allenai/WildBench
    export HF_BENCH_CONFIG=v2
    export HF_RESULTS_PATH=allenai/WildBench-V2-Model-Outputs
    eval_folder="eval_results/v2.1111/pairwise.v2/eval=${gpt_eval_name}/ref=${ref_name}/"
    local_result_file="result_dirs/wild_bench_v2/${model_name}.json"
elif [ $eval_config == "wbc" ]; then
    export HF_BENCH_PATH=allenai/WildBench
    export HF_BENCH_CONFIG=v2
    export HF_RESULTS_PATH=SAIL-Sailor/wildbench-v2-model-outputs # FIXME: add 4o and 4o-mini's results
    eval_folder="eval_results/v2.1111/pairwise.v2/eval=${gpt_eval_name}/ref=${ref_name}/"
    local_result_file="result_dirs/wild_bench_v2/${model_name}.json"
elif [ $eval_config == "sea" ]; then
    export HF_BENCH_PATH=sailor2/sea-wildbench
    export HF_RESULTS_PATH=SAIL-Sailor/sea-wildbench-v3-internal-model-outputs
    eval_folder="eval_results/v3.1130.sea/pairwise.v3/eval=${gpt_eval_name}/ref=${ref_name}/"
    local_result_file="result_dirs/sea_wild_bench_v3/${model_name}.json"
else
    echo "Invalid eval_config"
    exit 1
fi


mkdir -p $eval_folder 
eval_file="${eval_folder}/${model_name}.batch-submit.jsonl"

# judge if the eval_file exists 
if [ -f $eval_file ]; then
    echo "File $eval_file exists, skip generation"
    exit 0
fi

python src/eval.py \
    --batch_mode \
    --action eval \
    --model $gpt_eval_name \
    --max_words_to_eval 1000 \
    --mode pairwise \
    --eval_template $eval_template \
    --target_model_name $model_name \
    --ref_model_name $ref_name \
    --eval_output_file $eval_file \
    --local_result_file $local_result_file

echo "Batch results saved to $eval_file"
