import React, { useState } from "react";
import { Formik, Form, FormikState, Field } from "formik";
import { ResetPasswordData, SetPasswordData } from "../../../utils/interfaces";
import {
  resetPasswordValidation,
  resetPasswordInputs,
  setPasswordValidation,
  setPasswordInputs,
  customInputClasses,
} from "../../../utils/constants";
import { Input, Layout } from "../../shared";
import Markdown from "react-markdown";
import { postResetPassword, postSetPassword } from "../../../services/api";
import { successToast, errToast } from "../../../utils/functions/toast";
import jwt from "jsonwebtoken";
import Loading from "../../../utils/icons/loading";
import Footer from "../../shared/footer";

const ResetPassword = ({ action, queryToken }) => {
  //@ts-ignore
  const initialValuesReset: ResetPasswordData = {
    email: "",
  };
  //@ts-ignore
  const initialValuesSet: SetPasswordData = {
    password: "",
  };

  const [loading, setLoading] = useState<boolean>(false);

  const submitValuesReset = async (
    values: ResetPasswordData,
    resetForm: (nextState?: Partial<FormikState<ResetPasswordData>>) => void
  ) => {
    setLoading(true);
    const res = await postResetPassword(values);
    setLoading(false);
    if (res) {
      successToast("Please check your email!");
      resetForm({ values: { ...initialValuesReset } });
    }
  };

  const submitValuesSet = async (
    values: SetPasswordData,
    resetForm: (nextState?: Partial<FormikState<SetPasswordData>>) => void
  ) => {
    delete values.confirm_password;
    if (queryToken) {
      setLoading(true);
      var decodedToken = jwt.decode(queryToken);
      var dateNow = new Date();
      if (decodedToken.exp && decodedToken.exp > dateNow.getTime() / 1000) {
        const res = await postSetPassword(values, queryToken);
        if (res) {
          successToast("Password set successfully!");
          resetForm({ values: { ...initialValuesSet } });
          setLoading(false);
        }
      } else {
        errToast("Time to set password has expired");
        setLoading(false);
      }
    } else {
      errToast("You do not have access to set password!");
    }
  };

  return (
    <>
      <Layout type="maintainer">
        <h1 className="flex justify-center text-4xl font-extrabold text-white">
          {action === "set" ? "Set" : "Reset"} Your Password
        </h1>
        {action === "set" ? (
          <Formik
            initialValues={initialValuesSet}
            onSubmit={(values, { resetForm }) => {
              submitValuesSet(values, resetForm);
            }}
            validationSchema={setPasswordValidation}
            enableReinitialize
          >
            {({ errors, touched }) => (
              <Form className="flex flex-col px-6 lg:w-1/4 max-w-6xl mt-10 py-6 mx-auto bg-white rounded-lg">
                {setPasswordInputs.map((input, index) => (
                  <div
                    key={index}
                    className="border-2 border-gray-700 rounded my-4 p-4"
                  >
                    <Input key={input.id} {...input} {...customInputClasses} />
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
                    {loading ? (
                      <span className="flex w-6 mx-auto">
                        <Loading />
                      </span>
                    ) : (
                      "Submit"
                    )}
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
        ) : (
          <Formik
            initialValues={initialValuesReset}
            onSubmit={(values, { resetForm }) => {
              submitValuesReset(values, resetForm);
            }}
            validationSchema={resetPasswordValidation}
            enableReinitialize
          >
            {({ errors, touched }) => (
              <Form className="flex flex-col px-6 lg:w-1/4 max-w-6xl mt-10 py-6 mx-auto bg-white rounded-lg">
                {resetPasswordInputs.map((input) => (
                  <div className="border-2 border-gray-700 rounded my-4 p-4">
                    <Input key={input.id} {...input} {...customInputClasses} />
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
                    {loading ? (
                      <span className="flex w-6 mx-auto">
                        <Loading />
                      </span>
                    ) : (
                      "Submit"
                    )}
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
        )}
      </Layout>
      <div className="fixed bottom-0 w-full">
        <Footer />
      </div>
    </>
  );
};

export default ResetPassword;
