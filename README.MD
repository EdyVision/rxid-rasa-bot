# RxID Rasa Bot
A chatbot created with Rasa by EdyVision to help identify prescription drugs using the RxID Drug Search service, an NLM and OpenFDA client.

## Installation docs from Rasa
https://rasa.com/docs/rasa/installation

## Training and Testing

```bash
rasa train
```

After a successful training, execute the following to communicate with the bot.

```bash
rasa shell --debug
```

## Running the bot locally

The actions server will need to be running in a separate terminal window with the followng:

```bash
rasa run actions
```

To run the bot locally, use Rasa X

```bash
rasa x
```

