import React, { useState } from "react";
import { Formik, Form, FormikState } from "formik";
import { ResetPasswordData, SetPasswordData } from "../../../utils/interfaces";
import {
  resetPasswordValidation,
  resetPasswordInputs,
  setPasswordValidation,
  setPasswordInputs,
} from "../../../utils/constants";
import { Input, Layout } from "../../shared";
import { getRecaptchaToken } from "../../../services/recaptcha";
import instance from "../../../services/api";
import Markdown from "react-markdown";
import { postResetPassword } from "../../../services/api";
import { successToast } from "../../../utils/functions/toast";

const ResetPassword = ({ action, ...props }) => {
  const initialValues: SetPasswordData = {
    password: "",
    passwordConfirmation: "",
  };

  const [loading, setLoading] = useState<boolean>(true);

  const submitValues = async (
    values: ResetPasswordData,
    resetForm: (nextState?: Partial<FormikState<SetPasswordData>>) => void
  ) => {
    setLoading(true);
    const res = await postResetPassword(values);
    if (res) {
      successToast("Password changed successfully!");
      resetForm({ values: { ...initialValues } });
    }
  };

  return (
    <Layout type="maintainer">
      <h1 className="flex justify-center text-4xl font-extrabold text-white">
        {action === "set" ? "Set" : "Reset"} Your Password
      </h1>

      <Formik
        initialValues={initialValues}
        onSubmit={(values, { resetForm }) => submitValues(values, resetForm)}
        validationSchema={
          action === "reset" ? resetPasswordValidation : setPasswordValidation
        }
      >
        {({ errors, touched }) => (
          <Form className="flex flex-col px-6 w-1/4 max-w-6xl mt-10 py-6 mx-auto bg-white rounded-lg">
            {action === "set"
              ? setPasswordInputs.map((input) => (
                  <div className="border-2 border-gray-700 rounded my-4 p-4">
                    <Input key={input.id} {...input} />
                  </div>
                ))
              : resetPasswordInputs.map((input) => (
                  <div className="border-2 border-gray-700 rounded my-4 p-4">
                    <Input key={input.id} {...input} />
                  </div>
                ))}
            <div className="flex justify-center">
              <button
                disabled={Object.keys(errors).length > 0}
                type="submit"
                className={`${
                  Object.keys(errors).length > 0
                    ? "cursor-not-allowed bg-opacity-70"
                    : "cursor-pointer"
                } text-white bg-base-teal w-32 py-4 font-semibold rounded-lg`}
              >
                Submit
              </button>
            </div>
            {Object.keys(errors).map((error) => {
              if (touched[error]) {
                return (
                  <Markdown
                    key={error.trim()}
                    className="text-red-500 my-2 lg:my-1"
                  >
                    {errors[error] as string}
                  </Markdown>
                );
              }
            })}
          </Form>
        )}
      </Formik>
    </Layout>
  );
};

export default ResetPassword;
