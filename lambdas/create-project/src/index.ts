import { config } from "dotenv";
import { Handler } from "aws-lambda";

import {
  eventRequest,
  eventRequestSchema,
  eventResponse,
} from "./models/schema";
import { errors } from "./error/errors";
import validateQuery from "./services/validate-query";
import snsError from "./error/sns-error";

config();

const lambdaHandler: Handler<eventRequest, eventResponse> = async (
  event,
  context,
  callback
) => {
  try {
    await validateQuery(event, eventRequestSchema);
    return {
      success: true,
      "repo-link": "success",
      "team-slug": "nice-team",
      visibility: "public-or-private",
    };
  } catch (err) {
    if (err && err.message) {
      return {
        success: false,
        error: { ...err },
      };
    } else {
      await snsError("create-project", err);
      return {
        success: false,
        error: errors.GCSRM001,
      };
    }
  }
};

exports.handler = lambdaHandler;
