import sys
import nbformat

def convert_notebook_to_sql(ipynb_path, sql_path):
    with open(ipynb_path, 'r', encoding='utf-8') as ipynb_file:
        notebook = nbformat.read(ipynb_file, as_version=4)
    
    sql_commands = []
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            sql_commands.append(cell['source'])

    with open(sql_path, 'w', encoding='utf-8') as sql_file:
        sql_file.write('\n\n'.join(sql_commands))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_ipynb_to_sql.py <input.ipynb> <output.sql>")
        sys.exit(1)

    ipynb_path = sys.argv[1]
    sql_path = sys.argv[2]
    convert_notebook_to_sql(ipynb_path, sql_path)
    print(f"Converted {ipynb_path} to {sql_path}")
