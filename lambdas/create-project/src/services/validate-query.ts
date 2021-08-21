import * as yup from "yup";

import { eventRequest, eventRequestSchema } from "../models/schema";

/**
 * Query validator for Yup
 * @param {eventRequest} data The event data
 * @param {yup.ObjectSchema<any>} schema The validation schema
 */
const validateQuery = async (
  data: eventRequest,
  schema: yup.ObjectSchema<any> = eventRequestSchema
) => {
  try {
    await schema.validate(data, { abortEarly: false });
  } catch (error) {
    let message: string = "";
    error.errors.forEach((e: string) => {
      message += `${e}. `;
    });
    throw {
      name: "ValidationError",
      message,
    };
  }
};

export default validateQuery;
