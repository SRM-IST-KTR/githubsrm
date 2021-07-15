import React, { useEffect } from "react";
import { Formik, Form } from "formik";
import { ResetPasswordData } from "../../../utils/interfaces";
import {
  resetPasswordValidation,
  resetPasswordInputs,
} from "../../../utils/constants";
import { Input, Layout } from "../../shared";
import { getRecaptchaToken } from "../../../services/recaptcha";
import instance from "../../../services/api";
import { successToast, errToast } from "../../../utils/functions/toast";

const ResetPassword = () => {
  const initialValues: {
    srm_email: string;
    current_password: string;
    new_password: string;
  } = {
    srm_email: "",
    current_password: "",
    new_password: "",
  };

  const submitValues = async (values: ResetPasswordData) => {
    const token = sessionStorage.getItem("token");
    const recaptchaToken = await getRecaptchaToken("post");
    await instance
      .post("maintainer/reset-password", values, {
        headers: {
          Authorization: `Bearer ${token}`,
          "X-RECAPTCHA-TOKEN": recaptchaToken,
        },
      })
      .then((res) => {
        console.log(res.data, "reset");
        successToast("Password changed successfully!");
      })
      .catch((err) => {
        errToast(err.message);
      });
  };

  return (
    <Layout type="maintainer">
      <h1 className="flex justify-center text-4xl font-extrabold text-white">
        Reset Your Password
      </h1>

      <Formik
        initialValues={initialValues}
        onSubmit={submitValues}
        validationSchema={resetPasswordValidation}
      >
        <Form className="flex flex-col px-6 w-1/4 max-w-6xl mt-10 py-6 mx-auto bg-white rounded-lg">
          {resetPasswordInputs.map((input) => (
            <div className="border-2 border-gray-700 rounded my-4 p-4">
              <Input key={input.id} {...input} />
            </div>
          ))}
          <div className="flex justify-center">
            <button
              type="submit"
              className="rounded-xl font-bold items-center my-3 bg-base-teal p-3"
            >
              Submit
            </button>
          </div>
        </Form>
      </Formik>
    </Layout>
  );
};

export default ResetPassword;
