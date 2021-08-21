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
import {
  checkTeamExists,
  createChildTeam,
  createParentTeam,
} from "./services/github";
import { generateTeamID, generateYearID } from "./services/parsers";

config();

const lambdaHandler: Handler<eventRequest, eventResponse> = async (
  event,
  context,
  callback
) => {
  try {
    await validateQuery(event, eventRequestSchema);
    const yearID = await generateYearID(event.year);
    const checkYearExists = await checkTeamExists(yearID);
    let parentTeamID;
    if (checkYearExists === -1) {
      parentTeamID = await createParentTeam(yearID);
    } else {
      parentTeamID = checkYearExists;
    }
    const childTeamSlug = await generateTeamID(event["project-name"]);
    const childTeam = await createChildTeam(event, childTeamSlug, parentTeamID, yearID);
    return {
      success: true,
      "repo-link": "success",
      "team-slug": JSON.stringify(childTeam),
      visibility: `${parentTeamID}`,
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
