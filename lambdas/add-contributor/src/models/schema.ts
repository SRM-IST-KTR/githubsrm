import * as yup from "yup";

export const eventRequestSchema = yup
  .object({
    "team-slug": yup.string().trim().required(),
    contributor: yup.string().trim().required(),
  })
  .required();

export type eventRequest = yup.InferType<typeof eventRequestSchema>;

export interface successResponse {
  success: boolean;
  "team-slug": string;
  contributor: string;
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
