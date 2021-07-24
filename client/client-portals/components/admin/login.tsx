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
import { Input, Button } from "@/shared/index";
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
    <div className="md:p-14 bg-base-blue">
      <h1 className="flex justify-center text-4xl font-extrabold text-white mt-5">
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
              <div key={index} className="bg-gray-50 rounded my-4 px-2 py-1">
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
              <Button
                disabled={Object.keys(errors).length > 0}
                type="submit"
                btnStyle="primary"
              >
                {loading ? (
                  <span className="flex w-6 mx-auto">
                    <Loading />
                  </span>
                ) : (
                  "Login"
                )}
              </Button>
            </div>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default AdminLogin;
