import os
import re
import subprocess

nexus_folder = "/Users/victor_torres/Documents/MR_Bayes/mafft_nex"
iqtree_results_folder = "/Users/victor_torres/Documents/MR_Bayes/bestmodel_results"
output_dir = "/Users/victor_torres/Documents/MR_Bayes/results"

os.makedirs(output_dir, exist_ok=True)

model_map = {
    "JC": "lset nst=1;",
    "K2P": "lset nst=2;",
    "F81": "lset nst=1 statefreq=empirical;",
    "HKY": "lset nst=2;",
    "HKY+F": "lset nst=2 statefreq=empirical;",
    "HKY+G4": "lset nst=2 rates=gamma;",
    "HKY+I": "lset nst=2 rates=propinv;",
    "HKY+I+G4": "lset nst=2 rates=propinv gamma;",
    "HKY+F+G4": "lset nst=2 rates=gamma statefreq=empirical;",
    "HKY+F+I+G4": "lset nst=2 rates=propinv gamma statefreq=empirical;",

    "SYM": "lset nst=6;",
    "SYM+G4": "lset nst=6 rates=gamma;",
    "SYM+I": "lset nst=6 rates=propinv;",
    "SYM+I+G4": "lset nst=6 rates=propinv gamma;",

    "GTR": "lset nst=6;",
    "GTR+F": "lset nst=6 statefreq=empirical;",
    "GTR+G4": "lset nst=6 rates=gamma;",
    "GTR+I": "lset nst=6 rates=propinv;",
    "GTR+I+G4": "lset nst=6 rates=propinv gamma;",
    "GTR+F+G4": "lset nst=6 rates=gamma statefreq=empirical;",
    "GTR+F+I+G4": "lset nst=6 rates=propinv gamma statefreq=empirical;",

    "TN": "lset nst=6;",
    "TN+G4": "lset nst=6 rates=gamma;",
    "TN+I": "lset nst=6 rates=propinv;",
    "TN+I+G4": "lset nst=6 rates=propinv gamma;",

    "TrN": "lset nst=6;",
    "TrN+G4": "lset nst=6 rates=gamma;",
    "TrN+I": "lset nst=6 rates=propinv;",
    "TrN+I+G4": "lset nst=6 rates=propinv gamma;",

    "K3Pu": "lset nst=2;",
    "K3Pu+G4": "lset nst=2 rates=gamma;",
    "K3Pu+I": "lset nst=2 rates=propinv;",
    "K3Pu+I+G4": "lset nst=2 rates=propinv gamma;",
    "K3Pu+F": "lset nst=2 statefreq=empirical;",
    "K3Pu+F+G4": "lset nst=2 rates=gamma statefreq=empirical;",
    "K3Pu+F+I+G4": "lset nst=2 rates=propinv gamma statefreq=empirical;"
}

for filename in os.listdir(nexus_folder):
    if filename.endswith(".nex"):
        input_file = os.path.join(nexus_folder, filename)
        output_file = os.path.join(nexus_folder, filename.replace(".nex", "_fixed.nex"))

        print(f"Cleaning: {filename}: {output_file}")

        with open(input_file, "r") as infile, open(output_file, "w") as outfile:
            for line in infile:
                line = re.sub(r"\'", "", line)
                line = re.sub(r"\,", "", line)
                outfile.write(line)

        print(f"Fixed file saved as: {output_file}")

print("All NEXUS files have been cleaned.")

for filename in os.listdir(nexus_folder):
    if filename.endswith("_fixed.nex"):
        dataset_name = filename.replace("_fixed.nex", "")
        iqtree_file = os.path.join(iqtree_results_folder, f"{dataset_name}.iqtree")
        nexus_path = os.path.join(nexus_folder, filename)
        dataset_output_dir = os.path.join(output_dir, dataset_name)
        os.makedirs(dataset_output_dir, exist_ok=True)

        best_model = None
        if os.path.exists(iqtree_file):
            with open(iqtree_file, "r") as file:
                for line in file:
                    if "Best-fit model according to BIC:" in line:
                        best_model = line.split(":")[-1].strip()
                        break

        if best_model:
            print(f"Best model for {dataset_name}: {best_model}")
            mb_model_command = model_map.get(best_model, "lset nst=6 rates=gamma;")
        else:
            print(f"No model found for {dataset_name}. Using default (GTR+G).")
            mb_model_command = "lset nst=6 rates=gamma;"

        mb_script_path = os.path.join(dataset_output_dir, f"{dataset_name}_mrbayes.nex")

        mb_script = f"""
begin mrbayes;
    set autoclose=yes nowarn=yes;
    execute {nexus_path};
    {mb_model_command}
    prset statefreqpr=dirichlet(1,1,1,1);
    mcmc ngen=1000000 samplefreq=100 printfreq=100 diagnfreq=1000 nchains=4 nruns=2 burninfrac=0.25;
    sump;
    sumt;
end;
"""

        with open(mb_script_path, "w") as f:
            f.write(mb_script)

        print(f"MrBayes script created: {mb_script_path}")

        log_file = os.path.join(dataset_output_dir, f"{dataset_name}_mrbayes.log")
        with open(log_file, "w") as log:
            subprocess.run(["/opt/homebrew/bin/mb", mb_script_path], stdout=log, stderr=log)

        print(f"MrBayes analysis completed for: {dataset_name}")

print("All MrBayes analyses are finished.")
