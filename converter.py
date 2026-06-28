def limpar_aspas_csv_tab(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f_in, \
         open(output_file, "w", encoding="utf-8") as f_out:

        for line in f_in:
            # remove aspas duplas somente do início e do fim de cada campo
            campos = line.rstrip("\n").split("\t")

            campos_limpos = []
            for campo in campos:
                if campo.startswith('"') and campo.endswith('"'):
                    campo = campo[1:-1]   # remove aspas somente da ponta
                campos_limpos.append(campo)

            # monta a linha limpa novamente, com separação \t
            f_out.write("\t".join(campos_limpos) + "\n")


# Exemplo de uso:
limpar_aspas_csv_tab(
    input_file="tb_treina_cap44.csv",
    output_file="cap_44.csv"
)
