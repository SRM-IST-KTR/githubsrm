import * as yup from "yup";

export const eventRequestSchema = yup
  .object({
    "project-name": yup.string().trim().required(),
    "project-description": yup.string().trim().required(),
    year: yup
      .string()
      .trim()
      .matches(/^[0-9]{4}$/, "year should be 4-digit string")
      .required(),
    maintainers: yup
      .array()
      .of(yup.string().trim().required())
      .min(1, "maintainers array cannot be empty")
      .required(),
    private: yup.boolean().required(),
  })
  .required();

export type eventRequest = yup.InferType<typeof eventRequestSchema>;

export interface successResponse {
  success: boolean;
  "repo-link": string;
  "team-slug": string;
  visibility: string;
}

export interface errorResponse {
  error:
    | Error
    | {
        success: boolean;
        error:
          | {
              name: string;
              message: string;
            }
          | any;
      };
}

export type eventResponse = successResponse | errorResponse;
