import click
import cli.config
import cli.snakemake
import cli.shiny


@click.group()
def main():
    pass


@main.command(help='Create a config YAML file for running the Snakemake pipeline. Sample names are either passed as comma seperated lists or are read from text files if --use-sample-files parameter is set.')
@click.option('--use-sample-files', is_flag=True, default=False, help='Load sample names from text files instead of passing them as a comma-seperated list.')
@click.option('--genome_build', type=click.Choice(['hg19','hg38']), default='hg38', help='Build of the reference used for annotation.')
@click.option('--cores-per-job', default=1, help='The number of cores to use per job.')
@click.argument('fastq_dir')
@click.argument('reference_fasta')
@click.argument('group1')
@click.argument('group2')
@click.argument('output_dir')
@click.argument('target_yaml')
def create_config(use_sample_files, genome_build, cores_per_job, fastq_dir, reference_fasta, group1, group2, output_dir, target_yaml):

    cli.config.create_config(use_sample_files, genome_build, cores_per_job, fastq_dir, reference_fasta, group1, group2, output_dir, target_yaml)


@main.command(help='Run the snakemake pipeline using a config file.')
@click.option('--dry-run', is_flag=True, default=False, help='Only dry-run the workflow.')
@click.option('--cores', default=1, help='The number of cores to use for running the pipeline.')
@click.argument('config_yaml')
def run_snakemake_from_config(dry_run, cores, config_yaml):

    cli.snakemake.run_snakemake_from_config(dry_run, config_yaml, cores=cores)


@main.command(help='Run the Snakemake pipeline from command line. Sample names are either passed as comma seperated lists or are read from text files if --use-sample-files parameter is set.')
@click.option('--dry-run', is_flag=True, default=False, help='Only dry-run the pipeline.')
@click.option('--use-sample-files', is_flag=True, default=False, help='Load sample names from text files instead of passing them as a comma-seperated list.')
@click.option('--cores', default=1, help='The number of cores to use for running the pipeline.')
@click.option('--genome_build', type=click.Choice(['hg19','hg38']), default='hg38', help='Build of the reference used for annotation.')
@click.argument('fastq_dir')
@click.argument('reference_fasta')
@click.argument('group1')
@click.argument('group2')
@click.argument('output_dir')
def run_snakemake(dry_run, use_sample_files, cores, genome_build, fastq_dir, reference_fasta, group1, group2, output_dir):

    cli.snakemake.run_snakemake(dry_run, use_sample_files, cores, genome_build, fastq_dir, reference_fasta, group1, group2, output_dir)


@main.command(help='Remove all files generated by the pipeline. This includes reference genome indices, as well. Use with care!')
@click.option('--dry-run', is_flag=True, default=False, help='Only dry-run deleting the pipeline output.')
@click.argument('config_yaml')
@click.confirmation_option(prompt='Are you sure you want to delete all files generated by the pipeline (this includes reference indices)?')
def delete_all_output(dry_run, config_yaml):

    cli.snakemake.delete_all_output(dry_run, config_yaml)


@main.command(help='Start shiny GUI on folders generated by the snakemake pipeline.')
@click.option('--host', default="0.0.0.0", help="Host ip for shiny to listen on.")
@click.option('--port', default=9898, help='Shiny port number.')
@click.argument('project_dirs', nargs=-1, required=True)
def run_shiny(host, port, project_dirs):

    cli.shiny.start_shiny(project_dirs, host, port)
