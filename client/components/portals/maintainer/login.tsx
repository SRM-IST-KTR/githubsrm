import { useState } from 'react';
import { Formik, Form, FormikState } from 'formik';

import { MaintainerLoginData } from '../../../utils/interfaces';
import {
  maintainerLoginValidation,
  maintainerLoginInputs,
} from '../../../utils/constants';
import { Input } from '../../shared';

const MaintainerLogin = () => {
  const initialValues: MaintainerLoginData = {
    email: '',
    password: '',
  };

  const submitValues = (values: MaintainerLoginData) => {
    console.log(values);
  };

  return (
    <>
      <div className='flex justify-center mt-10'>
        <h1>Maintainer Login</h1>
      </div>

      <Formik
        initialValues={initialValues}
        onSubmit={submitValues}
        validationSchema={maintainerLoginValidation}>
        <Form className='w-full max-w-6xl mt-6 mx-auto'>
          {maintainerLoginInputs.map((input) => (
            <Input key={input.id} {...input} />
          ))}
          
        </Form>
      </Formik>
    </>
  );
};

export default MaintainerLogin;
