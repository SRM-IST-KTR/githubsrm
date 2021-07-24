import { Formik, Form, FormikState, Field } from "formik";
import React, { useState } from "react";
import { AdminRegisterData } from "utils/interfaces";
import Markdown from "react-markdown";
import {
  adminRegisterValidation,
  adminRegisterInputs,
  customInputClasses,
} from "utils/constants";
import { Input, Button } from "@/shared/index";
import { postAdminRegister } from "services/api";
import { successToast } from "utils/functions/toast";
import { Loading } from "@/icons/index";

const AdminRegister = () => {
  const [authToken, setAuthToken] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  //@ts-ignore
  const initialValues: AdminRegisterData = {
    email: "",
    password: "",
  };

  const submitValues = async (
    values: AdminRegisterData,
    resetForm: (nextState?: Partial<FormikState<AdminRegisterData>>) => void
  ) => {
    setLoading(true);
    const res = await postAdminRegister(values, authToken);
    if (res) {
      successToast("Admin registered successfully!");
      resetForm({ values: { ...initialValues } });
      setLoading(false);
    } else {
      setLoading(false);
    }
  };

  return (
    <div className="md:p-14 bg-base-blue">
      <h1 className="flex justify-center text-2xl md:text-4xl font-extrabold text-white mt-5 md:mt-0">
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
              <div key={input.id} className="bg-gray-50 rounded my-4 px-2 py-1">
                <Input {...input} {...customInputClasses} />
              </div>
            ))}
            <Field
              onChange={(e) => setAuthToken(e.target.value)}
              className="bg-gray-50 rounded my-2 px-2 py-2"
              type="password"
              name="token"
              label="Secret Key"
              placeholder="Secret Key"
            />
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
                  "Register"
                )}
              </Button>
            </div>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default AdminRegister;
