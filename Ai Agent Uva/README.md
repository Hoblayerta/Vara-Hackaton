Prerequisites

    Python 2.7+
    Node.js 23+
    pnpm

    Note for Windows Users: WSL 2 is required.

Use the Starter (Recommended)

git clone https://github.com/elizaos/eliza-starter.git
cd eliza-starter
cp .env.example .env
Edit .env and add your values:

# Suggested quickstart environment variables
DISCORD_APPLICATION_ID=  # For Discord integration
DISCORD_API_TOKEN=      # Bot token
HEURIST_API_KEY=       # Heurist API key for LLM and image generation
OPENAI_API_KEY=        # OpenAI API key
GROK_API_KEY=          # Grok API key
ELEVENLABS_XI_API_KEY= # API key from elevenlabs (for voice)
LIVEPEER_GATEWAY_URL=  # Livepeer gateway URL

Start the Agent

Inform it which character you want to run:
Copy paste uva.character.json

pnpm start --character="characters/Uva.character.json"

You can also load multiple characters with the characters option with a comma separated list:

pnpm start --characters="characters/trump.character.json,characters/tate.character.json"

Interact with the Agent

Now you're ready to start a conversation with your agent! Open a new terminal window

pnpm start:client

pnpm start:client

