import AWS from "aws-sdk";

/**
 * Send SNS Notification on unknown error
 * @param {string} scope The lambda function which is sending
 * @param {any} err The error object/message
 * @param {number} [maxRetries=5] Maximum retires on sending SNS topic
 */
const snsError = async (scope: string, err: any, maxRetries: number = 5) => {
  try {
    if (maxRetries > 0) {
      const sns = new AWS.SNS({
        credentials: {
          accessKeyId: process.env.ACCESS_KEY_ID!,
          secretAccessKey: process.env.SECRET_ACCESS_KEY!,
        },
        region: process.env.REGION!,
      });
      await sns
        .publish({
          Subject: `[LAMBDA-ERROR] Error on AWS lambda: '${scope}'`,
          TopicArn: process.env.SNS_ARN!,
          Message: JSON.stringify(
            {
              lambda: scope,
              error: { ...err },
            },
            null,
            "\t"
          ),
        })
        .promise();
    }
  } catch (error) {
    console.log("Error in SNS! Retrying...");
    snsError(scope, err, maxRetries - 1);
  }
};

export default snsError;
