"""Generate benchmarks graphs and RESULTS.md with benchmark results.

Usage:
  gen-benchmark-report [-i config.json] [--reports-dir=TEMPLATES_DIR] gen-plots <REPORTS>...
  gen-benchmark-report [-i config.json] [--reports-dir=TEMPLATES_DIR] [--img-dir=IMG_DIR] gen-results-md <REPORTS>...
  gen-benchmark-report -h | --help
  gen-benchmark-report --version

Commands:
  gen-plots                     plot graphs from reports
  gen-results-md                generate RESULTS.md from reports

Arguments:
  -i info.json                 .json config with framework infos [default: ./info.yml]
  --reports-dir=REPORTS_DIR    reports directory [default: ./reports/]
  --img-dir=IMG_DIR            images directory [default: img/]
  <REPORTS>...                 list of .json files from google benchmark

Options:
  -h, --help            show help
  -v, --version         show version

"""
from docopt import docopt
import plotly.express as px
import psutil as psu
import pandas as pd
import platform
import pystache
import os
import json
import re

RESULTS_MD_MUSTACHE_FILENAME = os.path.join(os.path.dirname(__file__), 'RESULTS.md.mustache')


def format_bytes(byte):
  for x in ['B', 'KB', 'MB', 'GB', 'TB']:
    if byte < 1024:
      return f"{byte:.2f}{x}"
    byte = byte/1024


def get_total_memory():
    mem = psu.virtual_memory()
    return format_bytes(mem.total)


def genPlots(frameworks_info, results):
    plot_data = {}
    for framework, result in results.items():
        if '_meta' != framework:
            for ek in result['entries'].keys():
                x = list(result['entries'][ek].keys())
                y = result['plot_data'][ek]
                output_png_filename = result['entries_data'][ek][0]['output_png_filename']
                unit = result['unit']
                name = frameworks_info[framework]['name']

                if ek not in plot_data:
                    plot_data[ek] = {}
                if 'df' not in plot_data[ek]:
                    plot_data[ek]['df'] = {}

                plot_data[ek]['df'][name] = y
                plot_data[ek]['df']['entities'] = x
                plot_data[ek]['output_png_filename'] = output_png_filename
                plot_data[ek]['unit'] = unit
                plot_data[ek]['name'] = name

    for key, data in plot_data.items():
        y = list(data['df'].keys())
        y.remove('entities')
        fig = px.line(data['df'], x="entities", y=y, labels={
             "value": "time ({})".format(data['unit']),
             "variable": "Frameworks",
         }, title=key, log_y=True)
        fig.write_image(data['output_png_filename'])


def genResultsMd(output_dir, frameworks_info, results, img_dir):
    results_md_filename = os.path.join(output_dir, 'RESULTS.md')
    data = {'candidates': [candidate for candidate in frameworks_info.values() if
                           'skip_candidate' not in candidate or not candidate['skip_candidate']],
            'environment': {'os': results['_meta']['os'], 'cpu': "{:.2f}GHz@{:d}Cores".format(results['_meta']['ghz_per_cpu'], results['_meta']['num_cpus']), 'ram': results['_meta']['ram']}}

    summary_df_data = {}
    df_data = {}
    df_index = {}
    for framework, result in results.items():
        if framework == '_meta':
            continue

        name = frameworks_info[framework]['name']
        summary_df_data[name] = []
        summary_df_index = []
        for ek, entries_data in result['entries_data'].items():
            if ek not in df_data:
                df_data[ek] = {}
            if ek not in df_index:
                df_index[ek] = []
            if name not in df_data[ek]:
                df_data[ek][name] = []

            if ek == 'SystemsUpdate':
                for edata in entries_data:
                    if edata['entities'] == 10000:
                        summary_df_data[name].append("{:.4f}s".format(edata['time_s']))
                        summary_df_index.append('Update  10k entities with 2 Systems')
                    elif edata['entities'] == 100000:
                        summary_df_data[name].append("{:.4f}s".format(edata['time_s']))
                        summary_df_index.append('Update 100k entities with 2 Systems')
                    elif edata['entities'] == 500000:
                        summary_df_data[name].append("{:.4f}s".format(edata['time_s']))
                        summary_df_index.append('Update 500k entities with 2 Systems')
                    elif edata['entities'] == 1000000:
                        summary_df_data[name].append("{:.4f}s".format(edata['time_s']))
                        summary_df_index.append('Update   1M entities with 2 Systems')

            if ek == 'CreateEntities':
                for edata in entries_data:
                    if edata['entities'] == 10000:
                        df_index[ek].append('Create  10k entities with two Components')
                        df_data[ek][name].append("{:.4f}s".format(edata['time_s']))
                    elif edata['entities'] == 100000:
                        df_index[ek].append('Create 100k entities with two Components')
                        df_data[ek][name].append("{:.4f}s".format(edata['time_s']))
                    elif edata['entities'] == 500000:
                        df_index[ek].append('Create 500k entities with two Components')
                        df_data[ek][name].append("{:.4f}s".format(edata['time_s']))
                    elif edata['entities'] == 1000000:
                        df_index[ek].append('Create   1M entities with two Components')
                        df_data[ek][name].append("{:.4f}s".format(edata['time_s']))
            elif ek == 'DestroyEntities':
                for edata in entries_data:
                    if edata['entities'] == 10000:
                        df_index[ek].append('Destroy  10k entities with two Components')
                        df_data[ek][name].append("{:.4f}s".format(edata['time_s']))
                    elif edata['entities'] == 100000:
                        df_index[ek].append('Destroy 100k entities with two Components')
                        df_data[ek][name].append("{:.4f}s".format(edata['time_s']))
                    elif edata['entities'] == 500000:
                        df_index[ek].append('Destroy 500k entities with two Components')
                        df_data[ek][name].append("{:.4f}s".format(edata['time_s']))
                    elif edata['entities'] == 1000000:
                        df_index[ek].add('Destroy   1M entities with two Components')
                        df_data[ek][name].append("{:.4f}s".format(edata['time_s']))
            elif ek == 'UnpackOneComponent':
                for edata in entries_data:
                    if edata['entities'] == 10000:
                        df_index[ek].append('Unpack one Component in  10k entities')
                        df_data[ek][name].append("{:.4f}s".format(edata['time_s']))
                    elif edata['entities'] == 100000:
                        df_index[ek].append('Unpack one Component in 100k entities')
                        df_data[ek][name].append("{:.4f}s".format(edata['time_s']))
                    elif edata['entities'] == 500000:
                        df_index[ek].append('Unpack one Component in 500k entities')
                        df_data[ek][name].append("{:.4f}s".format(edata['time_s']))
                    elif edata['entities'] == 1000000:
                        df_index[ek].append('Unpack one Component in   1M entities')
                        df_data[ek][name].append("{:.4f}s".format(edata['time_s']))
            elif ek == 'UnpackTwoComponents':
                for edata in entries_data:
                    if edata['entities'] == 10000:
                        df_index[ek].append('Unpack two Components in  10k entities')
                        df_data[ek][name].append("{:.4f}s".format(edata['time_s']))
                    elif edata['entities'] == 100000:
                        df_index[ek].append('Unpack two Components in 100k entities')
                        df_data[ek][name].append("{:.4f}s".format(edata['time_s']))
                    elif edata['entities'] == 500000:
                        df_index[ek].append('Unpack two Components in 500k entities')
                        df_data[ek][name].append("{:.4f}s".format(edata['time_s']))
                    elif edata['entities'] == 1000000:
                        df_index[ek].append('Unpack two Components in   1M entities')
                        df_data[ek][name].append("{:.4f}s".format(edata['time_s']))
            elif ek == 'UnpackThreeComponentsFromMixedEntities':
                for edata in entries_data:
                    if edata['entities'] == 10000:
                        df_index[ek].append('Unpack three Components in  10k entities')
                        df_data[ek][name].append("{:.4f}s".format(edata['time_s']))
                    elif edata['entities'] == 100000:
                        df_index[ek].append('Unpack three Components in 100k entities')
                        df_data[ek][name].append("{:.4f}s".format(edata['time_s']))
                    elif edata['entities'] == 500000:
                        df_index[ek].append('Unpack three Components in 500k entities')
                        df_data[ek][name].append("{:.4f}s".format(edata['time_s']))
                    elif edata['entities'] == 1000000:
                        df_index[ek].append('Unpack three Components in   1M entities')
                        df_data[ek][name].append("{:.4f}s".format(edata['time_s']))
            elif ek == 'SystemsUpdate':
                for edata in entries_data:
                    if edata['entities'] == 10000:
                        df_index[ek].append('Update  10k entities with 2 Systems')
                        df_data[ek][name].append("{:.4f}s".format(edata['time_s']))
                    elif edata['entities'] == 100000:
                        df_index[ek].append('Update 100k entities with 2 Systems')
                        df_data[ek][name].append("{:.4f}s".format(edata['time_s']))
                    elif edata['entities'] == 500000:
                        df_index[ek].append('Update 500k entities with 2 Systems')
                        df_data[ek][name].append("{:.4f}s".format(edata['time_s']))
                    elif edata['entities'] == 1000000:
                        df_index[ek].append('Update   1M entities with 2 Systems')
                        df_data[ek][name].append("{:.4f}s".format(edata['time_s']))
            elif ek == 'ComplexSystemsUpdate':
                for edata in entries_data:
                    if edata['entities'] == 10000:
                        df_index[ek].append('Update  10k entities with 3 Systems')
                        df_data[ek][name].append("{:.4f}s".format(edata['time_s']))
                    elif edata['entities'] == 100000:
                        df_index[ek].append('Update 100k entities with 3 Systems')
                        df_data[ek][name].append("{:.4f}s".format(edata['time_s']))
                    elif edata['entities'] == 500000:
                        df_index[ek].append('Update 500k entities with 3 Systems')
                        df_data[ek][name].append("{:.4f}s".format(edata['time_s']))
                    elif edata['entities'] == 1000000:
                        df_index[ek].append('Update   1M entities with 3 Systems')
                        df_data[ek][name].append("{:.4f}s".format(edata['time_s']))

    summary_df = pd.DataFrame(summary_df_data, index=summary_df_index)
    data['summary'] = {'table': summary_df.to_markdown(), 'figure_img_src': os.path.join(img_dir, 'SystemsUpdate.png'), 'figure_img_alt': 'Summary SystemsUpdate Plot'}

    data['plots'] = {}
    for ek, dfd in df_data.items():
        df = pd.DataFrame(dfd, index=list(dict.fromkeys((df_index[ek]))))
        data['plots'][ek] = {'table': df.to_markdown(), 'figure_img_src': os.path.join(img_dir, "{:s}.png".format(ek)), 'figure_img_alt': "{:s} Plot".format(ek)}

    with open(RESULTS_MD_MUSTACHE_FILENAME, 'r') as results_file:
        results_md_template = results_file.read()
        with open(results_md_filename, 'w') as results_md_file:
            results_md_file.write(pystache.render(results_md_template, data))

def main(args):
    #print(args)

    frameworks_info = {}
    if args['-i']:
        with open(args['-i'], 'r') as info_file:
            info_data = json.load(info_file)
            frameworks_info = info_data['frameworks']

    output_dir = os.path.abspath(args['--reports-dir']) if args['--reports-dir'] else os.path.abspath('.')

    #print(frameworks_info)

    reports = {}
    if args['<REPORTS>']:
        for report_filename in args['<REPORTS>']:
            with open(report_filename, 'r') as report_file:
                report_data = json.load(report_file)
                reports[report_data['context']['framework.name']] = report_data

    num_cpus = 0
    mhz_per_cpu = 0

    results = {}
    for framework, report in reports.items():
        num_cpus = report['context']['num_cpus']
        mhz_per_cpu = report['context']['mhz_per_cpu']
        version = report['context']['framework.version'] if 'framework.version' in report['context'] else None

        entries = {}
        entries_unit = None
        entries_data = {}
        for benchmark in report['benchmarks']:
            name = benchmark['name']
            time = benchmark['real_time']
            time_ns = None
            time_ms = None
            time_s = None
            entities = None
            entities_minimal = None
            entities_mo = None
            entities_mdo = None
            key = ''
            unit = benchmark['time_unit']
            if benchmark['time_unit'] == 'ns':
                time_ns = int(time)
                time_ms = time_ns / 1000000.0
                time_s = time_ms / 1000.0
            elif benchmark['time_unit'] == 'ms':
                time_ns = int(time * 1000000.0)
                time_ms = time
                time_s = time_ms / 1000.0

            if re.search(r'^BM_(.*)_CreateEntities\/', name):
                key = 'CreateEntities'
                entities = int(benchmark['entities'])
                entities_mo = int(benchmark['entities_mo']) if 'entities_mo' in benchmark else None
                entities_mdo = int(benchmark['entities_mdo']) if 'entities_mdo' in benchmark else None
            elif re.search(r'^BM_(.*)_DestroyEntities\/', name):
                key = 'DestroyEntities'
                entities = int(benchmark['entities'])
                entities_mo = int(benchmark['entities_mo']) if 'entities_mo' in benchmark else None
                entities_mdo = int(benchmark['entities_mdo']) if 'entities_mdo' in benchmark else None
            elif re.search(r'^BM_(.*)_UnpackOneComponent\/', name):
                key = 'UnpackOneComponent'
                entities = int(benchmark['entities'])
                entities_mo = int(benchmark['entities_mo']) if 'entities_mo' in benchmark else None
                entities_mdo = int(benchmark['entities_mdo']) if 'entities_mdo' in benchmark else None
            elif re.search(r'^BM_(.*)_UnpackTwoComponents\/', name):
                key = 'UnpackTwoComponents'
                entities = int(benchmark['entities'])
                entities_mo = int(benchmark['entities_mo']) if 'entities_mo' in benchmark else None
                entities_mdo = int(benchmark['entities_mdo']) if 'entities_mdo' in benchmark else None
            elif re.search(r'^BM_(.*)_UnpackTwoComponentsFromMixedEntities\/', name):
                key = 'UnpackTwoComponentsFromMixedEntities'
                entities = int(benchmark['entities'])
                entities_minimal = int(benchmark['entities_minimal']) if 'entities_minimal' in benchmark else None
                entities_mo = int(benchmark['entities_mo']) if 'entities_mo' in benchmark else None
                entities_mdo = int(benchmark['entities_mdo']) if 'entities_mdo' in benchmark else None
            elif re.search(r'^BM_(.*)_UnpackThreeComponentsFromMixedEntities\/', name):
                key = 'UnpackThreeComponentsFromMixedEntities'
                entities = int(benchmark['entities'])
                entities_minimal = int(benchmark['entities_minimal']) if 'entities_minimal' in benchmark else None
                entities_mo = int(benchmark['entities_mo']) if 'entities_mo' in benchmark else None
                entities_mdo = int(benchmark['entities_mdo']) if 'entities_mdo' in benchmark else None
            elif re.search(r'^BM_(.*)_SystemsUpdate\/', name):
                key = 'SystemsUpdate'
                entities = int(benchmark['entities'])
                entities_minimal = int(benchmark['entities_minimal']) if 'entities_minimal' in benchmark else None
                entities_mo = int(benchmark['entities_mo']) if 'entities_mo' in benchmark else None
                entities_mdo = int(benchmark['entities_mdo']) if 'entities_mdo' in benchmark else None
            elif re.search(r'^BM_(.*)_ComplexSystemsUpdate\/', name):
                key = 'ComplexSystemsUpdate'
                entities = int(benchmark['entities'])
                entities_minimal = int(benchmark['entities_minimal']) if 'entities_minimal' in benchmark else None
                entities_mo = int(benchmark['entities_mo']) if 'entities_mo' in benchmark else None
                entities_mdo = int(benchmark['entities_mdo']) if 'entities_mdo' in benchmark else None

            if key:
                if key not in entries:
                    entries[key] = {}
                entries[key][entities] = time_ms
                entries_unit = 'ms'
                output_png_filename = os.path.join(output_dir, "{:s}.png".format(key))
                if key not in entries_data:
                    entries_data[key] = []
                entries_data[key].append({'name': name, 'unit': unit, 'time': time, 'time_ns': time_ns, 'time_ms': time_ms, 'time_s': time_s, 'entities': entities, 'entities_minimal': entities_minimal, 'entities_mo': entities_mo, 'entities_mdo': entities_mdo, 'output_png_filename': output_png_filename})

        result_plot_data = {}
        for k in entries.keys():
            sorted(entries_data[k], key=lambda e: e['entities'])
            result_plot_data[k] = []
            for m in sorted(entries[k].keys()):
                result_plot_data[k].append(entries[k][m])
        name = frameworks_info[framework]['name']
        results[framework] = {'entries': entries, 'entries_data': entries_data, 'plot_data': result_plot_data, 'unit': entries_unit, 'framework': framework, 'label': name, 'version': version}

    results['_meta'] = {'ghz_per_cpu': mhz_per_cpu / 1000.0, 'mhz_per_cpu': mhz_per_cpu, 'num_cpus': num_cpus, 'os': platform.system(), 'ram': get_total_memory()}

    if args['gen-plots']:
        genPlots(frameworks_info, results)
    elif args['gen-results-md']:
        genResultsMd(output_dir, frameworks_info, results, args['--img-dir'])


if __name__ == '__main__':
    args = docopt(__doc__)
    main(args)

