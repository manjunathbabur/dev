import json
import os

def convert_ipynb_to_sql(notebook_path, output_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    sql_statements = []
    for cell in notebook.get('cells', []):
        if cell.get('cell_type') == 'code':
            source = ''.join(cell.get('source', []))
            if source.strip().lower().startswith(('select', 'insert', 'update', 'delete', 'create', 'drop')):
                sql_statements.append(source)

    if sql_statements:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(sql_statements))

def main():
    notebooks_dir = './notebooks'
    for file_name in os.listdir(notebooks_dir):
        if file_name.endswith('.ipynb'):
            notebook_path = os.path.join(notebooks_dir, file_name)
            output_path = os.path.join(notebooks_dir, file_name.replace('.ipynb', '.sql'))
            convert_ipynb_to_sql(notebook_path, output_path)

if __name__ == "__main__":
    main()
