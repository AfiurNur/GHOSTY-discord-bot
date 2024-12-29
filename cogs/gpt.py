import discord
from discord.ext import commands
from discord import app_commands
import openai
import secret

class gptCog(commands.Cog):
    """Cog to handle GPT AI interaction."""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="gpt", description="Chat with an AI!")
    @app_commands.guilds(discord.Object(id=1242396018704908289))  # Replace with your guild ID
    async def gpt(self, interaction: discord.Interaction, prompt: str):
        """Slash command to chat with an AI."""
        try:
            # Set the OpenAI API key
            openai.api_key = secret.open_ai_api_key
            
            # Use the newer ChatCompletion endpoint
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Use gpt-4 if available
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100  # Limit token usage
            )
            
            # Extract and send the response
            result = response["choices"][0]["message"]["content"].strip()
            await interaction.response.send_message(result)

        except Exception as e:
            # Handle any errors
            await interaction.response.send_message(f"An error occurred: {e}")

    @app_commands.command(name="gpt_test", description="Test if the GPT cog is working successfully!")
    async def gpt_test(self, interaction: discord.Interaction):
        """Test command to ensure the GPT cog is working."""
        await interaction.response.send_message("The GPT cog is working successfully!")

# Setup function to add this cog
async def setup(bot):
    await bot.add_cog(gptCog(bot))
