import React, { useContext } from "react";
import { Formik, Form } from "formik";
import Router from "next/router";
import { AdminLoginData } from "../../utils/interfaces";
import { adminLoginValidation, adminLoginInputs } from "../../utils/constants";
import { Input } from "../shared";
import instance from "../../services/api";
import { successToast, errToast } from "../../utils/functions/toast";
import { AuthContext } from "../../context/AuthContext";
import { getRecaptchaToken } from "../../services/recaptcha";

const AdminLogin = () => {
  const authContext = useContext(AuthContext);

  const initialValues: { email: string; password: string } = {
    email: "",
    password: "",
  };

  const submitValues = async (values: AdminLoginData) => {
    const recaptchaToken = await getRecaptchaToken("post");
    await instance
      .post("admin/login", values, {
        headers: {
          "X-RECAPTCHA-TOKEN": recaptchaToken,
        },
      })
      .then(async (res) => {
        sessionStorage.setItem("token", res.data.keys);
        authContext.decode();
        successToast("Logged In successfully!");
        Router.push("admin/dashboard");
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
        onSubmit={submitValues}
        validationSchema={adminLoginValidation}
      >
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
              type="submit"
              className="rounded-xl font-bold items-center my-3 bg-base-teal p-3"
            >
              Log In
            </button>
          </div>
        </Form>
      </Formik>
    </div>
  );
};

export default AdminLogin;
