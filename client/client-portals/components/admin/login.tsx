import React, { useContext, useState } from "react";
import { Formik, Form, FormikState } from "formik";
import Router from "next/router";
import Markdown from "react-markdown";
import { AdminLoginData } from "utils/interfaces";
import {
  adminLoginValidation,
  adminLoginInputs,
  customInputClasses,
} from "utils/constants";
import { Input, Footer } from "@/shared/index";
import { successToast } from "utils/functions/toast";
import { AuthContext } from "context/authContext";
import { postAdminLogin } from "services/api";
import { Loading } from "@/icons/index";

const AdminLogin = () => {
  const authContext = useContext(AuthContext);
  const [loading, setLoading] = useState<boolean>(false);

  //@ts-ignore
  const initialValues: AdminLoginData = {
    email: "",
    password: "",
  };

  const submitValues = async (
    values: AdminLoginData,
    resetForm: (nextState?: Partial<FormikState<AdminLoginData>>) => void
  ) => {
    setLoading(true);
    const res = await postAdminLogin(values);
    if (res) {
      authContext.decode();
      successToast("Logged In successfully!");
      Router.push("admin/dashboard");
      setLoading(false);
      resetForm({ values: { ...initialValues } });
    } else {
      setLoading(false);
    }
  };

  return (
    <>
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
              {adminLoginInputs.map((input, index) => (
                <div
                  key={index}
                  className="border-2 border-gray-700 rounded my-4 p-4"
                >
                  <Input key={input.id} {...input} {...customInputClasses} />
                </div>
              ))}
              {Object.keys(errors).map((error) => {
                if (touched[error]) {
                  return (
                    <Markdown
                      key={error.trim()}
                      className="text-red-500 my-2 lg:my-2"
                    >
                      {errors[error] as string}
                    </Markdown>
                  );
                }
              })}
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
                    "Login"
                  )}
                </button>
              </div>
            </Form>
          )}
        </Formik>
      </div>
      <div className="fixed bottom-0 w-full">
        <Footer />
      </div>
    </>
  );
};

export default AdminLogin;
