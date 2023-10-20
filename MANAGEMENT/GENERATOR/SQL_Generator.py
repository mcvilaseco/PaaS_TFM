from jinja2 import Environment, FileSystemLoader
import json
import click
import os

@click.command()
@click.option(
    '--template',
    required=True,
    #type=click.Path(exists=True),
    help="Jinja2 template file"
)

@click.option(
    '--data',
    '-d',
    required=True,
    #type=click.Path(exists=True),
    help="JSON data file"
)

def main(template, data):
    #Load jinja2 enviroment
    env = Environment(loader=FileSystemLoader('MANAGEMENT/GENERATOR/TEMPLATES'))
    jinja_template = env.get_template(template)
    
    # Read JSON data
    data_file_path = f'MANAGEMENT/GENERATOR/DATA/{data}'
    with open(data_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    # Apply data to the Jinja2 template
    output = jinja_template.render(json_data)

    # Show resultant SQL query
    print(output)

     # Save output.sql file
    with open('output.sql', 'w') as output_file:
        output_file.write(output)
    
    #output_file_path = os.path.join(os.path.dirname(__file__), 'output.sql')
    #with open(output_file_path, 'w') as output_file:
    #    output_file.write(output)

if __name__ == "__main__":
    main()
