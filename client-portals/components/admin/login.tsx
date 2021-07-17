import React, { useContext } from "react";
import { Formik, Form, FormikState } from "formik";
import Router from "next/router";
import Markdown from "react-markdown";
import { AdminLoginData } from "../../utils/interfaces";
import { adminLoginValidation, adminLoginInputs } from "../../utils/constants";
import { Input } from "../shared";
import instance from "../../services/api";
import { successToast, errToast } from "../../utils/functions/toast";
import { AuthContext } from "../../context/AuthContext";
import { getRecaptchaToken } from "../../services/recaptcha";

const AdminLogin = () => {
  const authContext = useContext(AuthContext);

  const initialValues: AdminLoginData = {
    email: "",
    password: "",
  };

  const submitValues = async (
    values: AdminLoginData,
    resetForm: (nextState?: Partial<FormikState<AdminLoginData>>) => void
  ) => {
    const recaptchaToken = await getRecaptchaToken("post");
    await instance
      .post("admin/login", values, {
        headers: {
          "X-RECAPTCHA-TOKEN": recaptchaToken,
        },
      })
      .then((res) => {
        sessionStorage.setItem("token", res.data.keys);
        authContext.decode();
        successToast("Logged In successfully!");
        Router.push("admin/dashboard");
        resetForm({ values: { ...initialValues } });
      })
      .catch((err) => {
        errToast(err.message);
      });
  };

  return (
    <div className="min-h-screen p-14 bg-base-blue">
      <h1 className="flex justify-center text-4xl font-extrabold text-white">
        Admin Login
      </h1>

      <Formik
        initialValues={initialValues}
        onSubmit={(values, { resetForm }) => submitValues(values, resetForm)}
        validationSchema={adminLoginValidation}
      >
        {({ errors, touched }) => (
          <Form className="flex flex-col px-6 lg:w-1/4 max-w-6xl mt-10 py-6 mx-auto bg-white rounded-lg">
            {adminLoginInputs.map((input) => (
              <div
                key={input.id}
                className="border-2 border-gray-700 rounded my-4 p-4"
              >
                <Input {...input} />
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
    </div>
  );
};

export default AdminLogin;
