import { Formik, Form } from 'formik';

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
    <div className='min-h-screen p-14 bg-base-blue'>
      <h1 className='flex justify-center text-4xl font-extrabold text-white'>
        Maintainer Login
      </h1>

      <Formik
        initialValues={initialValues}
        onSubmit={submitValues}
        validationSchema={maintainerLoginValidation}>
        <Form className='flex flex-col px-6 w-1/4 max-w-6xl mt-10 py-6 mx-auto bg-white rounded-lg'>
          {maintainerLoginInputs.map((input) => (
            <div className='border border-black rounded my-4 p-4'>
              <Input key={input.id} {...input} />
            </div>
          ))}
          <div className='flex justify-center'>
            <button
              type='submit'
              className='rounded-xl font-bold items-center my-3 bg-base-teal p-3'>
              Submit
            </button>
          </div>
        </Form>
      </Formik>
    </div>
  );
};

export default MaintainerLogin;
