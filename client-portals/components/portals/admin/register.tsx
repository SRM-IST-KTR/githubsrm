import { Formik, Form } from "formik";
import React, { useState } from "react";
import { AdminRegisterData } from "../../../utils/interfaces";
import {
  adminRegisterValidation,
  adminRegisterInputs,
} from "../../../utils/constants";
import { Input } from "../../shared";
import instance from "../../../services/api";

const AdminRegister = () => {
  const [token, setToken] = useState("");

  const initialValues: { email: string; password: string } = {
    email: "",
    password: "",
  };

  const submitValues = (values: AdminRegisterData) => {
    instance
      .post("/admin/register", values, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        console.log(res);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  return (
    <div className="min-h-screen p-14 bg-base-blue">
      <h1 className="flex justify-center text-4xl font-extrabold text-white">
        Admin Registration
      </h1>

      <Formik
        initialValues={initialValues}
        onSubmit={submitValues}
        validationSchema={adminRegisterValidation}
      >
        <Form className="flex flex-col px-6 w-1/4 max-w-6xl mt-10 py-6 mx-auto bg-white rounded-lg">
          {adminRegisterInputs.map((input) => (
            <div className="border-2 border-gray-700 rounded my-4 p-4">
              <Input key={input.id} {...input} />
            </div>
          ))}
          <div className="flex justify-center">
            <button
              type="submit"
              className="rounded-xl font-bold items-center my-3 bg-base-teal p-3"
            >
              Register
            </button>
          </div>
        </Form>
      </Formik>
    </div>
  );
};

export default AdminRegister;
