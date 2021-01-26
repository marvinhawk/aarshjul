import pandas as pd
import matplotlib.pyplot as plt
import json
import os

def main():
    
    # Setup data paths.
    settings_file = "settings.json"
    events_file = "events.csv"

    # Set output file name.
    plot_filename = "aarshjul.png"

    # Check for existing plots.
    plot_file = increment_filename(plot_filename)

    # Load settings.
    with open(settings_file, encoding='utf-8') as f:
        settings = json.loads(f.read())
    
    # Load event data.
    events = pd.read_csv(events_file)
    events = events.fillna('')
    events['colour'] = events.apply(lambda x: colour_events(x, settings['colours']), axis=1)

    # Draw plots and save to output file.
    draw_plot(settings, events, plot_file)

def colour_events(row, colours):
    if row['name']:
        return colours['events']
    else:
        return colours['background']

def increment_filename(name, out_dir='plots', n=1):
    """ Helper function to avoid overwriting existing files.
    """

    new_name = f'{name.split(".")[0]}{n:02}.png'

    if new_name in os.listdir(out_dir):
        n += 1
        return increment_filename(name, out_dir, n)
    else:
        return f'{out_dir}/{new_name}'

def draw_plot(settings, events, out_file):

    params = settings['layout']
    colours = settings['colours']
    months = settings['months']

    # Extract data from activities.
    activity_names = [i['name'] for i in settings['activities']]
    activity_weights = [i['week_duration'] for i in settings['activities']]
    activity_categories = [i['category'] for i in settings['activities']]



    fig, ax = plt.subplots()

    # Events plot
    #draw_layer() #TODO
    ax.pie( events['weight'],
            labels=events['name'],
            radius=params['size'] + params['event_adjustment'],
            colors=events['colour'],
            wedgeprops=dict(width=params['width'] + params['event_adjustment'], edgecolor=colours['background']),
            textprops=dict(va='center', rotation_mode='anchor', size=12, color=colours['background']),
            startangle=90,
            counterclock=False,
            labeldistance=0.78,
            rotatelabels=True
            )

    # Activities plot
    #draw_layer() #TODO
    act_wedges, act_labels = ax.pie(activity_weights,
                                    labels=activity_names,
                                    radius=params['size'] - params['width'],
                                    colors=[colours[c] for c in activity_categories],
                                    wedgeprops=dict(width=params['width'], edgecolor=colours['background']),
                                    textprops=dict(va='center', rotation_mode='anchor', size=14, color=colours['text_contrast']),
                                    startangle=90 - params['offset'] * 360,
                                    counterclock=False,
                                    labeldistance=0.87,
                                    rotatelabels=True
                                    )

    # Adjust activites labels
    for label in act_labels:
        if label.get_text() == 'Sommerferie':
            label.set_rotation('horizontal')
        label.set_va('center')
        label.set_ha('center')

    # Calendar plot
    #draw_layer() #TODO

    cal_wedges, cal_labels = ax.pie(months['weights'],
                                    labels=months['names'],
                                    radius=params['size'] - params['width'] * 2,
                                    colors=[colours['month1'], colours['month2']],
                                    wedgeprops=dict(width=params['width']/2, edgecolor=colours['background']),
                                    startangle=90,
                                    counterclock=False,
                                    labeldistance=0.9,
                                    rotatelabels=False
                                    )

    # Adjust calendar labels
    for ea, eb in zip(cal_wedges, cal_labels):
        mean_angle =(ea.theta1 + ea.theta2) / 2.
        
        eb.set_rotation(mean_angle + 270)
        eb.set_va("center")
        eb.set_ha("center")

    # Centre plot
    ax.pie([1],radius=params['size'] - params['width'] * 3, autopct=settings['title'], pctdistance=0, textprops=dict(size=28, color=colours['background']), colors=[colours['centre']])

    plt.savefig(out_file, bbox_inches='tight')
    print(f'Plot successfully saved to {out_file}.')


if __name__ == '__main__':
    main()