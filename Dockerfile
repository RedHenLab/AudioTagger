# Creation of base OS image
# FROM debian:bullseye-slim
FROM tensorflow/tensorflow:2.9.0-gpu

RUN apt-get -y update

RUN apt-get install --assume-yes --no-install-recommends --quiet \
        python3 \
        python3-pip \
        ffmpeg

RUN pip install --no-cache --upgrade pip setuptools
    
# Set working directory to MultiModalTVShowSeg-2022
WORKDIR /TaggingAudioEffects

# Copying the folder into the local
ADD ./tagging_audio_effects .

# View contents while building dockerfile
RUN ls -a

#RUN  python3 tools/audio_generation.py /mnt/rds/redhen/gallina/tv/2022 . "wav" "mp4" 1


# Install local dependencies
# RUN cd ..

#RUN pip3 install -r requirements.txt


# Remove copied folder
RUN rm -f -r ./tagging_audio_effects

#ADD . /mypackage/

#ENTRYPOINT ["python", "-m", "mypackage.script"]
