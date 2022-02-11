import Axios from "axios";
import FormData from "form-data";
/**
 * Send Discord Notification on unknown error
 * @param {string} scope The lambda function which is sending
 * @param {any} err The error object/message
 * @param {number} [maxRetries=5] Maximum retires on sending Discord Webhook
 */
const discordError = async (
  scope: string,
  err: any,
  maxRetries: number = 5
) => {
  try {
    const formData = new FormData();
    formData.append(
      "content",
      `:red_circle::yellow_circle: **Lambda Error Occurred!** :red_circle::yellow_circle:\n\n**SCOPE:** \`${scope}\`\n`
    );
    formData.append("files[0]", JSON.stringify(err, null, 4), "error.json");
    if (maxRetries > 0) {
      await Axios.post(process.env.DISCORD_WEBHOOK!, formData, {
        headers: formData.getHeaders(),
      });
    }
  } catch (error) {
    console.log("Error in Discord! Retrying...");
    discordError(scope, err, maxRetries - 1);
  }
};

export default discordError;
