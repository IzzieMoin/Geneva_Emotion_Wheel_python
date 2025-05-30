import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge
from tkinter import simpledialog

RATED_EMOTIONS = {}
EMOTIONS = ['Pleasure', 'Joy', 'Pride', 'Amusement', 'Interest', 'Anger', 'Hate', 'Contempt',
            'Disgust', 'Fear', 'Disappointment', 'Shame', 'Regret', 'Guilt', 'Sadness',
            'Compassion', 'Relief', 'Admiration','Love', 'Contentment']
def show_geneva_emotion_wheel():
    intensity_levels = ['1', '2', '3', '4', '5']

    fig, ax = plt.subplots(figsize=(8.5, 8.5))
    ax.set_aspect('equal')

    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)

    emotion_circles = []

    for i, emotion in enumerate(EMOTIONS):
        if i % 2 == 0:
            base_color = 'white'
        else:
            base_color = 'grey'
           
        for j, intensity in enumerate(intensity_levels):
            size = 0.135 + j * 0.05  
            angle = i * 360 / len(EMOTIONS)
            angle_rad = np.radians(angle)

            r = 1.0 + j * 0.65

            x = r * np.cos(angle_rad)
            y = r * np.sin(angle_rad)

            color = base_color

            circle = Circle((x, y), radius=size, facecolor=color, edgecolor='black', label=f"{emotion} ({intensity})")

            ax.add_patch(circle)
            emotion_circles.append((emotion, intensity, circle, base_color))

        label_x = (r + 1.1) * np.cos(angle_rad)
        label_y = (r + 0.6) * np.sin(angle_rad)

        ax.text(label_x, label_y, emotion, horizontalalignment='center', verticalalignment='center', fontsize=10)

        
    no_emotion_felt = Wedge((0, 0), 0.6, 0, 180, facecolor='lightgray', edgecolor='black', label='None Emotions')
    other_emotion_felt = Wedge((0, 0), 0.6, 180, 360, facecolor='white', edgecolor='black', label='Other Emotions')

    ax.add_patch(no_emotion_felt)
    ax.add_patch(other_emotion_felt)

    emotion_circles.append(('None Emotions', "None", no_emotion_felt, 'lightgray'))
    emotion_circles.append(('Other Emotions', "None", other_emotion_felt, 'white'))

    
    ax.text(0, 0.25, 'None', horizontalalignment='center', verticalalignment='center', fontsize=12, color='black')
    ax.text(0, -0.25, 'Other', horizontalalignment='center', verticalalignment='center', fontsize=12, color='black')

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim([-4, 4])
    ax.set_ylim([-4, 4])

    ax.set_title('What emotions did the audio clip make you feel? Please select the emotion(s) and mark the intensity of the selected emotion(s).', fontsize=14, pad=40)

    def onclick(event):
        if event.inaxes is not None:
            for emotion, intensity, circle, original_color in emotion_circles:
                if isinstance(circle, Wedge):
                    if circle.contains_point((event.x, event.y)):
                       
                        if emotion == 'None Emotions':
                            if RATED_EMOTIONS.get('None Emotions'):
                                circle.set_facecolor('white')
                                RATED_EMOTIONS.pop('None Emotions', None)
                            else:
                                for em, int_lv, circ, orig_color in emotion_circles:
                                    if em != 'None Emotions':  
                                        circ.set_facecolor(orig_color)
                                        RATED_EMOTIONS.pop(em, None)
                                circle.set_facecolor('lightblue')
                                RATED_EMOTIONS['None Emotions'] = 'Selected'
                            fig.canvas.draw()
                            break
                        elif emotion == 'Other Emotions':
                            if RATED_EMOTIONS.get('Other Emotions'):
                                circle.set_facecolor('lightgrey')
                                RATED_EMOTIONS.pop('Other Emotions', None)
                            else:
                                for em, int_lv, circ, ori_c in emotion_circles:
                                    if em == 'None Emotions':
                                        circ.set_facecolor(ori_c)
                                        RATED_EMOTIONS.pop(em, None)
                                circle.set_facecolor('lightblue')
                                description = 0
                                RATED_EMOTIONS['Other Emotions'] = description

                                custom_emotion = simpledialog.askstring("Custom Emotion", "Please enter your emotion with the intensity (1-5):\n format(emotion_intensity)")
                                print(f"custom_emotion: {custom_emotion}")
                                if custom_emotion != "" and custom_emotion is not None:
                                    RATED_EMOTIONS['Other Emotions'] = f"{custom_emotion}"
                                else:
                                    RATED_EMOTIONS['Other Emotions'] = 0
                                    circle.set_facecolor(original_color)
                            fig.canvas.draw()
                            break
                        else:
                            if RATED_EMOTIONS.get(emotion) == intensity:
                                circle.set_facecolor(original_color)
                                RATED_EMOTIONS.pop(emotion, None)
                            else:
                                if emotion in RATED_EMOTIONS:
                                    prev_intensity = RATED_EMOTIONS[emotion]
                                    for em, int_lv, circ, ori_c in emotion_circles:
                                        if em == emotion and int_lv == prev_intensity:
                                            circ.set_facecolor(ori_c)
                                            break
                                circle.set_facecolor('lightblue')
                                RATED_EMOTIONS[emotion] = intensity
                            fig.canvas.draw()
                            break
                elif isinstance(circle, Circle):
                    if circle.contains_point((event.x, event.y)):
                        if RATED_EMOTIONS.get(emotion) == intensity:
                            circle.set_facecolor(original_color)
                            RATED_EMOTIONS.pop(emotion, None)
                        else:
                            if emotion in RATED_EMOTIONS:
                                prev_intensity = RATED_EMOTIONS[emotion]
                                for em, int_lv, circ, ori_c in emotion_circles:
                                    if em == emotion and int_lv == prev_intensity:
                                        circ.set_facecolor(ori_c)
                                        break
                            circle.set_facecolor('lightblue')
                            RATED_EMOTIONS[emotion] = intensity
                            for em, int_lv, circ, orig_color in emotion_circles:
                                if em == "None Emotions":
                                    circ.set_facecolor('lightgrey')
                                    RATED_EMOTIONS.pop(em, None)
                        fig.canvas.draw()
                        break

    fig.canvas.mpl_connect('button_press_event', onclick)

    return fig

show_geneva_emotion_wheel()
plt.show()