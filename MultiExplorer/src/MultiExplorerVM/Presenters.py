import copy
import Tkinter
import numpy as np
from typing import Dict, Tuple
from ..GUI.Widgets import CanvasTable
from ..GUI.Presenters import Presenter, PlotbookPresenter
from matplotlib.figure import Figure


class CloudSimPresenter(Presenter):
    
    def __init__(self):
        super(CloudSimPresenter, self).__init__()

        self.table = None

        self.canvas_frame = None

    def present_results(self, frame, results, options=None):
        # todo
        return 0

    def present_partials(self, frame, step_results, options=None):
        raise NotImplementedError

    def get_info(self, step_results, options=None):
        
        simulation_preview = (
            "Time: {} hours\n"
            "Price: {} USD/h\n"
        ).format('%.2e' % step_results['original_time'], '%.2e' % round(step_results['original_price'], 2)
)
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

        sorted_solution = results['dsdse']['sorted_bruteforce']

        #solutions_filtered = self.get_bf_filtered_results(solutions)

        #nbr_of_solutions = len(solutions_filtered)

        nbr_of_solutions = len(sorted_solution)

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

        table_options['nbr_of_columns'] = 3

        solutions_data = [
            ['Architecture', 'Predicted cost (USD/h)', 'Predicted time (hours)'],
        ]

        #for s in solutions_filtered:
        for s in sorted_solution:
            solutions_data.append([
                s,
                '%.2e' % round(solutions[s]['cost_pred'], 10),
                "%.2e" % round(float(solutions[s]['time_pred']), 10)
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


class NSGATablePresenter(Presenter):
    
    def __init__(self):
        
        super(NSGATablePresenter, self).__init__()

        self.canvas = None

        self.og_table = None

        self.sol_table = None

    def present_partials(self, frame, step_results, options=None):
        raise NotImplementedError

    def present_results(self, frame, results, options=None):
        
        if 'nsga_solutions' not in results['dsdse']:
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

        solutions = results['dsdse']['nsga_solutions']

        sorted_solution = results['dsdse']['sorted_nsga']

        nbr_of_solutions = len(sorted_solution)

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

        table_options['nbr_of_columns'] = 3

        solutions_data = [
            ['Architecture', 'Predicted cost (USD/h)', 'Predicted time (hours)'],
        ]

        for s in sorted_solution:
            solutions_data.append([
                s,
                '%.2e' % round(solutions[s]['cost_pred'], 10),
                "%.2e" % round(float(solutions[s]['time_pred']), 10),
            ])

        table_options['data'] = solutions_data

        self.sol_table = CanvasTable(self.canvas, table_options)

        return height

    def get_info(self, step_results, options=None):
        raise NotImplemented


class NSGAPresenter(PlotbookPresenter):
    
    figsize = (12, 4)

    dpi = 100

    bar_height = .7

    ticks_font_size = 7

    bar_text_font_size = 9

    axis_font_size = 12

    time_color = 'darkblue'

    price_color = 'red'

    def get_figures(self, results):

        population_results = results['dsdse']['nsga_solutions']

        filtered_population = results['dsdse']['sorted_nsga']

        original_time = results['cloudsim']['original_time']

        original_price = results['cloudsim']['original_price']

        return {
            "NSGA-II Approximated Paretto Set": self.plot_population(
                population_results, # mostrando o total
                original_time,
                original_price,
                filtered_population
            )
        }

    def get_info(self, step_results, options=None):
        
        return (
                "NSGA-II generated a paretto frontier aproximation containing "
                + str(len(step_results['nsga_solutions']))
                + " distinct points."
        )

    def present_partials(self, frame, step_results, options=None):
        raise NotImplementedError

    @staticmethod
    def get_pd_performance_points(population_results, filtered_solutions):
        solutions = population_results.keys()

        points = []

        for key in filtered_solutions:
            solution = population_results[key]

            points.append((
                float(solution['cost_pred']),
                solution['time_pred'],
                solution['title']
            ))

        return points

    @staticmethod
    def plot_population(population_results, original_time, original_price, filtered_solutions):
        
        # type: (Dict, Tuple, Tuple) -> Figure
        points = NSGAPresenter.get_pd_performance_points(population_results, filtered_solutions)

        price_values, time_values, titles = zip(*points)

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

        time_bars = ax2.barh(ind * 2 + .5 * height, time_values, height, align='center',
                                    color=NSGAPresenter.time_color)

        for bar in time_bars:
            ax2.text(
                bar.get_x() + bar.get_width(),
                bar.get_y() + bar.get_height() * .5,
                '%.2e' % round(bar.get_width(), 10),
                ha='left',
                va='center',
                fontsize=NSGAPresenter.bar_text_font_size,
                color=NSGAPresenter.time_color
            )

        price_bars = ax.barh(ind * 2 - .5 * height, price_values,
                                     height=height, align='center', color=NSGAPresenter.price_color)

        for bar in price_bars:
            ax.text(
                bar.get_x() + bar.get_width(),
                bar.get_y() + bar.get_height() * .5,
                '%.2e' % round(bar.get_width(), 10),
                ha='left',
                va='center',
                fontsize=NSGAPresenter.bar_text_font_size,
                color=NSGAPresenter.price_color
            )

        ax2.set_xlabel("Predicted time (hours)", fontsize=NSGAPresenter.axis_font_size)

        ax.set_xlabel("Predicted cost (USD/h)", fontsize=NSGAPresenter.axis_font_size)

        ax2.axvline(x=original_time, color=NSGAPresenter.time_color)

        ax.axvline(x=original_price, color=NSGAPresenter.price_color)

        ylim = ax2.get_ylim()

        ax2.text(
            original_time,
            ylim[1] * .99,
            '%.2e' % round(original_time, 10),
            ha='left',
            va='top',
            fontsize=NSGAPresenter.bar_text_font_size * 5 / 6,
            color=NSGAPresenter.time_color
        )

        xlim = ax.get_xlim()

        ax.text(
            original_price + .001 * xlim[1],
            ylim[0],
            '%.2e' % round(original_price, 10),
            ha='left',
            va='bottom',
            fontsize=NSGAPresenter.bar_text_font_size * 5 / 6,
            color=NSGAPresenter.price_color
        )

        fig.subplots_adjust(
            top=0.8,
            bottom=0.2,
            left=0.2,
            right=0.95
        )

        return fig


class BruteForcePresenter(PlotbookPresenter):
    
    figsize = (12, 4)

    dpi = 100

    bar_height = .7

    ticks_font_size = 7

    bar_text_font_size = 9

    axis_font_size = 12

    time_color = 'darkblue'

    price_color = 'red'

    def get_figures(self, results):

        population_results = results['dsdse']['brute_force_solutions']

        filtered_population = results['dsdse']['sorted_bruteforce']

        original_time = results['cloudsim']['original_time']

        original_price = results['cloudsim']['original_price']

        return {
            "Brute Force Approximated Paretto Set": self.plot_population(
                population_results,
                original_time,
                original_price,
                filtered_population
            )
        }

    def present_partials(self, frame, step_results, options=None):
        raise NotImplementedError

    @staticmethod
    def get_pd_performance_points(population_results, filtred_solutions):
        
        solutions = population_results.keys()

        points = []

        for key in filtred_solutions:
            solution = population_results[key]

            points.append((
                float(solution['cost_pred']),
                solution['time_pred'],
                solution['title']
            ))

        return points

    @staticmethod
    def plot_population(population_results, original_time, original_price, filtered_solutions):
        
        # type: (Dict, Tuple, Tuple) -> Figure
        points = BruteForcePresenter.get_pd_performance_points(population_results, filtered_solutions)

        price_values, time_values, titles = zip(*points)

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

        time_bars = ax2.barh(ind * 2 + .5 * height, time_values, height, align='center',
                                    color=BruteForcePresenter.time_color)

        for bar in time_bars:
            ax2.text(
                bar.get_x() + bar.get_width(),
                bar.get_y() + bar.get_height() * .5,
                '%.2e' % round(bar.get_width(), 10),
                ha='left',
                va='center',
                fontsize=BruteForcePresenter.bar_text_font_size,
                color=BruteForcePresenter.time_color
            )

        price_bars = ax.barh(ind * 2 - .5 * height, price_values,
                                     height=height, align='center', color=BruteForcePresenter.price_color)

        for bar in price_bars:
            ax.text(
                bar.get_x() + bar.get_width(),
                bar.get_y() + bar.get_height() * .5,
                '%.2e   ' % round(bar.get_width(), 10),
                ha='left',
                va='center',
                fontsize=BruteForcePresenter.bar_text_font_size,
                color=BruteForcePresenter.price_color
            )

        ax2.set_xlabel("Predicted time (hours)", fontsize=BruteForcePresenter.axis_font_size)

        ax.set_xlabel("Predicted cost (USD/h)", fontsize=BruteForcePresenter.axis_font_size)

        ax2.axvline(x=original_time, color=BruteForcePresenter.time_color)

        ax.axvline(x=original_price, color=BruteForcePresenter.price_color)

        ylim = ax2.get_ylim()

        ax2.text(
            original_time,
            ylim[1] * .99,
            '%.2e' % round(original_time, 10),
            ha='left',
            va='top',
            fontsize=BruteForcePresenter.bar_text_font_size * 5 / 6,
            color=BruteForcePresenter.time_color
        )

        xlim = ax.get_xlim()

        ax.text(
            original_price + .001 * xlim[1],
            ylim[0],
            '%.2e' % round(original_price, 10),
            ha='left',
            va='bottom',
            fontsize=BruteForcePresenter.bar_text_font_size * 5 / 6,
            color=BruteForcePresenter.price_color
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
