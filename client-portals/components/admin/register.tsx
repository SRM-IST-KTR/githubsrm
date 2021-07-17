import { Formik, Form, FormikState, Field } from "formik";
import React, { useState } from "react";
import { AdminRegisterData } from "../../utils/interfaces";
import Markdown from "react-markdown";
import {
  adminRegisterValidation,
  adminRegisterInputs,
} from "../../utils/constants";
import { Input } from "../shared";
import { postAdminRegister } from "../../services/api";
import { successToast } from "../../utils/functions/toast";

const AdminRegister = () => {
  const [authToken, setAuthToken] = useState<string>("");
  const [loding, setLoading] = useState<boolean>(true);

  const initialValues: AdminRegisterData = {
    email: "",
    password: "",
  };

  const submitValues = async (
    values: AdminRegisterData,
    resetForm: (nextState?: Partial<FormikState<AdminRegisterData>>) => void
  ) => {
    setLoading(true);
    const authToken = sessionStorage.getItem("token");
    const res = await postAdminRegister(values, authToken);
    if (res) {
      successToast("Admin registered successfully!");
      resetForm({ values: { ...initialValues } });
    }
  };

  return (
    <div className="min-h-screen p-14 bg-base-blue">
      <h1 className="flex justify-center text-4xl font-extrabold text-white">
        Admin Registration
      </h1>

      <Formik
        initialValues={initialValues}
        onSubmit={(values, { resetForm }) => submitValues(values, resetForm)}
        validationSchema={adminRegisterValidation}
      >
        {({ errors, touched }) => (
          <Form className="flex flex-col px-6 lg:w-1/4 max-w-6xl mt-10 py-6 mx-auto bg-white rounded-lg">
            {adminRegisterInputs.map((input) => (
              <div
                key={input.id}
                className="border-2 border-gray-700 rounded my-4 p-4"
              >
                <Input {...input} />
              </div>
            ))}
            <Field
              onChange={(e) => setAuthToken(e.target.value)}
              className="border-2 border-gray-800 rounded-md p-3 mt-3"
              type="password"
              name="token"
              label="Secret Key"
              placeholder="Secret Key"
            />
            <div className="flex justify-center">
              <button
                disabled={Object.keys(errors).length > 0}
                type="submit"
                className={`${
                  Object.keys(errors).length > 0
                    ? "cursor-not-allowed bg-opacity-70"
                    : "cursor-pointer"
                } text-white bg-base-teal w-32 py-4 my-3 font-semibold rounded-lg`}
              >
                Register
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

export default AdminRegister;
