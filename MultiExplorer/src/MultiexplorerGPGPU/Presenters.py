import Tkinter

import numpy as np
from typing import Dict, Tuple
from matplotlib.figure import Figure
from scipy.interpolate import interp1d
from MultiExplorer.src.GUI.Presenters import Presenter, PlotbookPresenter
from MultiExplorer.src.GUI.Widgets import CanvasTable
import copy

brute_force_values = {}

class GPGPUSimPresenter(Presenter):
    
    def __init__(self):
        super(GPGPUSimPresenter, self).__init__()

        self.table = None

        self.canvas_frame = None


    def present_results(self, frame, results, options=None):
        # todo
        return 0


    def present_partials(self, frame, step_results, options=None):
        raise NotImplementedError


    def get_info(self, step_results, options=None):
        
        simulation_preview = (
            "Simulation time: {} sec\n"
            "Instruction rate: {} (inst/sec)\n"
            "Cycles rate: {} (cycle/sec)"
        ).format(str(step_results['simulation_time']), str(step_results['simulation_instructions_rate']), str(step_results['simulation_cycles_rate']))

        return simulation_preview


class BruteForceTablePresenter(Presenter):

    def get_info(self, step_results, options=None):
        
        if 'brute_force_solutions' not in step_results:
            return ""

        return (
                "The brute force algorithm found "
                + str(len(step_results['brute_force_solutions']))
                + " solutions."
        )


    def __init__(self):
        
        super(BruteForceTablePresenter, self).__init__()

        self.canvas = None

        self.sol_table = None


    def present_partials(self, frame, step_results, options=None):
        raise NotImplementedError


    def present_results(self, frame, results, options=None):
        
        if 'brute_force_solutions' not in results['dsdse']:
            return 0

        cell_height = 25

        table_options = {
            'pos': (2, 3*(cell_height+2)),
            'cells_width': [250, 250, 250],
            'font_height': 12,
            'cell_height': cell_height,
            'nbr_of_columns': 3,
            'nbr_of_rows': 6,
            'center': False,
        }

        self.canvas = Tkinter.Canvas(frame)

        solutions = results['dsdse']['brute_force_solutions']

        solutions_filtered = self.get_bf_filtered_results(solutions)

        nbr_of_solutions = len(solutions_filtered)

        height = table_options['cell_height'] * (6 + nbr_of_solutions + 6)

        self.canvas.config(width=options['width'], height=height)

        self.canvas.pack(
            fill=Tkinter.BOTH,
            expand=True
        )

        
        if results['dsdse']['solution_status']['is_viable']:
            text = "Viable Solutions Found through Brute Force (respected restrictions)"
        else:
            text = "No viable solutions found; brute force solutions did not respect all restrictions."


        self.canvas.create_text(2, 2*(cell_height+2), text=text,
                                anchor=Tkinter.NW)

        table_options['cells_width'] = [445, 145, 140, 140]

        table_options['nbr_of_rows'] = nbr_of_solutions + 1

        table_options['nbr_of_columns'] = 4

        solutions_data = [
            ['Architecture', 'Performance', 'Area', 'Power Density'],
        ]

        for s in solutions_filtered:
            solutions_data.append([
                s,
                str(round(solutions[s]['performance'], 2)) + " s^-1",
                str(round(solutions[s]['total_area'], 2)) + " mm^2",
                str(round(solutions[s]['power_density'], 2)) + " W/mm^2",
            ])

        table_options['data'] = solutions_data

        self.sol_table = CanvasTable(self.canvas, table_options)

        return height


    def get_bf_filtered_results(self, solutions):

        removed = self.remove_duplicate_solutions(solutions)

        for i in removed:
            del solutions[i]

        solutions_filtered = [key for key, value in sorted(solutions.items(), key=lambda sol: float(sol[1]['performance']), reverse=True)[:10]]

        self.filter_brute_force_results(solutions, solutions_filtered)

        return solutions_filtered


    def filter_brute_force_results(self, solutions, top10):

        global brute_force_values

        #counter = 0
        #for key, value in solutions.items():
        #    brute_force_values[key] = copy.deepcopy(value)
        #    counter += 1
        #    if counter == 5:
        #        break

        counter = 0
        for solution in top10:
            brute_force_values[solution] = copy.deepcopy(solutions[solution])
            counter += 1
            if counter == 5:
                break


    def remove_duplicate_solutions(self, solutions):
        
        final_solutions = []
        removed_solutions = []

        for solution in solutions:
            temp = solution.split()
            temp[0], temp[1], temp[3], temp[4] = temp[3], temp[4], temp[0], temp[1]
            if (" ".join(temp)) not in final_solutions:
                final_solutions.append(solution)
            else:
                removed_solutions.append(solution)

        # excluir depois
        for solution in removed_solutions:
            print(solution)

        return removed_solutions
    

class NSGAPresenter(PlotbookPresenter):
    
    figsize = (12, 4)

    dpi = 100

    bar_height = .7

    ticks_font_size = 7

    bar_text_font_size = 9

    axis_font_size = 12

    perf_color = 'darkblue'

    density_color = 'red'

    def get_figures(self, results):

        population_results = results['dsdse']['solutions']

        original_performance = results['dsdse']['performance_simulation']['performance']

        original_power_density = results['dsdse']['performance_simulation']['power_density']

        return {
            "NSGA-II Approximated Paretto Set": self.plot_population(
                population_results,
                original_performance,
                original_power_density
            )
        }


    def get_info(self, step_results, options=None):
        
        return (
                "NSGA-II generated a paretto frontier aproximation containing "
                + str(len(step_results['solutions']))
                + " distinct points."
        )


    def present_partials(self, frame, step_results, options=None):
        raise NotImplementedError

    @staticmethod
    def get_pd_performance_points(population_results):
        solutions = population_results.keys()

        points = []

        for key in population_results:
            solution = population_results[key]

            points.append((
                round(solution['power_density'], 2),
                round(float(solution['performance']), 2),
                solution['title']
            ))

        return points

    @staticmethod
    def plot_population(population_results, original_performance, original_power_density):
        
        # type: (Dict, Tuple, Tuple) -> Figure
        points = NSGAPresenter.get_pd_performance_points(population_results)

        power_density_values, performance_values, titles = zip(*points)

        nbr_of_solutions = len(titles)

        ind = np.arange(nbr_of_solutions)
        height = NSGAPresenter.bar_height

        fig = Figure(figsize=NSGAPresenter.figsize, dpi=NSGAPresenter.dpi)

        ax = fig.add_subplot(111)

        ax.set_yticks(range(0, int(nbr_of_solutions) * 2, 2))

        ax.set_yticklabels(titles, wrap=True, fontdict={'fontsize': NSGAPresenter.ticks_font_size,
                                                        'verticalalignment': 'center',
                                                        'horizontalalignment': 'right'})

        ax2 = ax.twiny()

        performance_bars = ax2.barh(ind * 2 + .5 * height, performance_values, height, align='center',
                                    color=NSGAPresenter.perf_color)

        for bar in performance_bars:
            ax2.text(
                bar.get_x() + bar.get_width(),
                bar.get_y() + bar.get_height() * .5,
                '%.2f' % round(bar.get_width(), 2),
                ha='left',
                va='center',
                fontsize=NSGAPresenter.bar_text_font_size,
                color=NSGAPresenter.perf_color
            )

        power_density_bars = ax.barh(ind * 2 - .5 * height, power_density_values,
                                     height=height, align='center', color=NSGAPresenter.density_color)

        for bar in power_density_bars:
            ax.text(
                bar.get_x() + bar.get_width(),
                bar.get_y() + bar.get_height() * .5,
                '%.2f' % round(bar.get_width(), 2),
                ha='left',
                va='center',
                fontsize=NSGAPresenter.bar_text_font_size,
                color=NSGAPresenter.density_color
            )

        ax2.set_xlabel("Performance (1/s)", fontsize=NSGAPresenter.axis_font_size)

        ax.set_xlabel("Power Density (W/mm^2)", fontsize=NSGAPresenter.axis_font_size)

        ax2.axvline(x=original_performance[0], color=NSGAPresenter.perf_color)

        ax.axvline(x=original_power_density[0], color=NSGAPresenter.density_color)

        ylim = ax2.get_ylim()

        ax2.text(
            original_performance[0],
            ylim[1] * .99,
            '%.2f' % round(original_performance[0], 2),
            ha='left',
            va='top',
            fontsize=NSGAPresenter.bar_text_font_size * 5 / 6,
            color=NSGAPresenter.perf_color
        )

        xlim = ax.get_xlim()

        ax.text(
            original_power_density[0] + .001 * xlim[1],
            ylim[0],
            '%.2f' % round(original_power_density[0], 2),
            ha='left',
            va='bottom',
            fontsize=NSGAPresenter.bar_text_font_size * 5 / 6,
            color=NSGAPresenter.density_color
        )

        fig.subplots_adjust(
            top=0.8,
            bottom=0.2,
            left=0.2,
            right=0.95
        )

        return fig


class NSGATablePresenter(Presenter):
    
    def __init__(self):
        
        super(NSGATablePresenter, self).__init__()

        self.canvas = None

        self.og_table = None

        self.sol_table = None


    def present_partials(self, frame, step_results, options=None):
        raise NotImplementedError


    def present_results(self, frame, results, options=None):
        
        if 'solutions' not in results['dsdse']:
            return 0

        cell_height = 25

        table_options = {
            'pos': (2, 3*(cell_height+2)),
            'cells_width': [250, 250, 250],
            'font_height': 12,
            'cell_height': cell_height,
            'nbr_of_columns': 3,
            'nbr_of_rows': 6,
            'center': False,
        }

        self.canvas = Tkinter.Canvas(frame)

        solutions = results['dsdse']['solutions']

        nbr_of_solutions = len(solutions)

        height = table_options['cell_height'] * (6 + nbr_of_solutions + 6)

        self.canvas.config(width=options['width'], height=height)

        self.canvas.pack(
            fill=Tkinter.BOTH,
            expand=True
        )


        self.canvas.create_text(2, 2*(cell_height+2), text="NSGA-II Generated Architectures",
                                anchor=Tkinter.NW)


        table_options['cells_width'] = [445, 145, 140, 140]

        table_options['nbr_of_rows'] = nbr_of_solutions + 1

        table_options['nbr_of_columns'] = 4

        solutions_data = [
            ['Architecture', 'Performance', 'Area', 'Power Density'],
        ]

        for s in solutions:
            solutions_data.append([
                s,
                str(round(float(solutions[s]['performance']), 2)) + " s^-1",
                str(round(float(solutions[s]['total_area']), 2)) + " mm^2",
                str(round(float(solutions[s]['power_density']), 2)) + " W/mm^2",
            ])

        table_options['data'] = solutions_data

        self.sol_table = CanvasTable(self.canvas, table_options)

        return height


    def get_info(self, step_results, options=None):
        raise NotImplemented
    

class BruteForcePresenter(PlotbookPresenter):
    
    figsize = (12, 4)

    dpi = 100

    bar_height = .7

    ticks_font_size = 7

    bar_text_font_size = 9

    axis_font_size = 12

    perf_color = 'darkblue'

    density_color = 'red'

    def get_figures(self, results):

        #population_results = results['dsdse']['brute_force_solutions']
        global brute_force_values
        
        population_results = copy.deepcopy(brute_force_values)

        brute_force_values.clear()

        original_performance = results['dsdse']['performance_simulation']['performance']

        original_power_density = results['dsdse']['performance_simulation']['power_density']

        return {
            "Brute Force Approximated Paretto Set": self.plot_population(
                population_results,
                original_performance,
                original_power_density
            )
        }


    def present_partials(self, frame, step_results, options=None):
        raise NotImplementedError

    @staticmethod
    def get_pd_performance_points(population_results):
        
        solutions = population_results.keys()

        points = []

        for key in population_results:
            solution = population_results[key]

            points.append((
                round(solution['power_density'], 2),
                round(float(solution['performance']), 2),
                solution['title']
            ))

        return points

    @staticmethod
    def plot_population(population_results, original_performance, original_power_density):
        
        # type: (Dict, Tuple, Tuple) -> Figure
        points = BruteForcePresenter.get_pd_performance_points(population_results)

        power_density_values, performance_values, titles = zip(*points)

        nbr_of_solutions = len(titles)

        ind = np.arange(nbr_of_solutions)
        height = BruteForcePresenter.bar_height

        fig = Figure(figsize=BruteForcePresenter.figsize, dpi=BruteForcePresenter.dpi)

        ax = fig.add_subplot(111)

        ax.set_yticks(range(0, int(nbr_of_solutions) * 2, 2))

        ax.set_yticklabels(titles, wrap=True, fontdict={'fontsize': BruteForcePresenter.ticks_font_size,
                                                        'verticalalignment': 'center',
                                                        'horizontalalignment': 'right'})

        ax2 = ax.twiny()

        performance_bars = ax2.barh(ind * 2 + .5 * height, performance_values, height, align='center',
                                    color=BruteForcePresenter.perf_color)

        for bar in performance_bars:
            ax2.text(
                bar.get_x() + bar.get_width(),
                bar.get_y() + bar.get_height() * .5,
                '%.2f' % round(bar.get_width(), 2),
                ha='left',
                va='center',
                fontsize=BruteForcePresenter.bar_text_font_size,
                color=BruteForcePresenter.perf_color
            )

        power_density_bars = ax.barh(ind * 2 - .5 * height, power_density_values,
                                     height=height, align='center', color=BruteForcePresenter.density_color)

        for bar in power_density_bars:
            ax.text(
                bar.get_x() + bar.get_width(),
                bar.get_y() + bar.get_height() * .5,
                '%.2f' % round(bar.get_width(), 2),
                ha='left',
                va='center',
                fontsize=BruteForcePresenter.bar_text_font_size,
                color=BruteForcePresenter.density_color
            )

        ax2.set_xlabel("Performance (1/s)", fontsize=BruteForcePresenter.axis_font_size)

        ax.set_xlabel("Power Density (W/mm^2)", fontsize=BruteForcePresenter.axis_font_size)

        ax2.axvline(x=original_performance[0], color=BruteForcePresenter.perf_color)

        ax.axvline(x=original_power_density[0], color=BruteForcePresenter.density_color)

        ylim = ax2.get_ylim()

        ax2.text(
            original_performance[0],
            ylim[1] * .99,
            '%.2f' % round(original_performance[0], 2),
            ha='left',
            va='top',
            fontsize=BruteForcePresenter.bar_text_font_size * 5 / 6,
            color=BruteForcePresenter.perf_color
        )

        xlim = ax.get_xlim()

        ax.text(
            original_power_density[0] + .001 * xlim[1],
            ylim[0],
            '%.2f' % round(original_power_density[0], 2),
            ha='left',
            va='bottom',
            fontsize=BruteForcePresenter.bar_text_font_size * 5 / 6,
            color=BruteForcePresenter.density_color
        )

        fig.subplots_adjust(
            top=0.8,
            bottom=0.2,
            left=0.2,
            right=0.95
        )

        return fig

    # Arrumar depois... super
    def present_results(self, frame, results, options=None):

        if 'brute_force_solutions' not in results['dsdse']:
            return 0
        else:

            #super(BruteForcePresenter, self).present_results(frame, results, options)
            figures = self.get_figures(results)

            if not figures:
                # nothing to present
                return

            self.create_plotbook(frame, options)

            for title in figures:
                self.add_plot(title, figures[title])

            return PlotbookPresenter.PLOTBOOK_HEIGHT + 20


    def get_info(self, step_results, options=None):
        raise NotImplemented