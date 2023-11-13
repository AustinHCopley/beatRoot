# beatRoot
Submitted to [HackUMass XI](https://hackumass-xi.devpost.com/)

## Inspiration
We wanted to create a DJ that can recommend songs based on the 'feel' of a song but is curated to support an activity you want to do like studying, walking, meditation, etc.
During the activity, we wanted the DJ to measure our emotional/mental state and recommend songs accordingly.

## What it does
The user will enter a song they like and a target activity.
Then, BeatRoot uses the heart rate sensor to get an understanding of physical/mental state and recommend songs based on the reference song and target activity.
The goal of BeatRoot is to create a constantly evolving playlist that will help maintain the optimal heart rate (thereby mental state).
Similar to the way the sympathetic and parasympathetic nervous systems will counteract each other to achieve homeostasis, we dynamically adjust the parameters for playlist creation to smoothly transition you from your current state to your desired state.
This dynamically created playlist can directly play through a connected device on Spotify at all times. 

## How we built it
We curated multiple song profiles to suit each activity in order to target heart rate, tempo, energy, etc. using Spotify API.
We used an Arduino Uno with a pulse sensor to get heart rate readings.
The song recommendation was assisted by our CNN-based song spectrogram feature extraction methodology.
