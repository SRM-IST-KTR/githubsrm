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
import discordError from "./error/discord-error";
import { addContributor } from "./services/github";

import { parseTeamSlug } from "./services/parsers";

config();

const lambdaHandler: Handler<eventRequest, eventResponse> = async (
  event,
  context,
  callback
) => {
  try {
    await validateQuery(event, eventRequestSchema);
    const teamInfo = parseTeamSlug(event["team-slug"]);
    await addContributor(teamInfo, event.contributor);
    return {
      success: true,
      contributor: event.contributor,
      "team-slug": event["team-slug"],
    };
  } catch (err: any) {
    await discordError("add-contributor", err);
    if (err && err.message) {
      return {
        success: false,
        error: {
          name: `CUSTOM_ERROR: ${err.message}`,
          message: JSON.stringify(err),
        },
      };
    } else {
      await snsError("add-contributor", err);
      return {
        success: false,
        error: errors.GCSRM001,
      };
    }
  }
};

exports.handler = lambdaHandler;
