Overview
========

Example usage of astrocloud locally using a local docker-desktop kubernetes cluster to run a csv writer with a csv uploader sidecar.
It is assumed that you already have homebrew installed and that you have your docker desktop kubernetes cluster running.


Deploy Your Project Locally
===========================

1. If you do not already have astrocloud install then run `make install-astro`

2. To run the example: `make`
   1. First builds a docker container to use for the python examples
   2. Configures the local kubeconfig to use with astro
   3. Start the astro dev server
   4. Trigger the example dag via astrocloud command
   5. Wait a bit for the container to spin up
   6. Watch the logs for the sidecar container
   7. Optionally you can open another shell and run `make watch-base` to also follow the main logs

Access to the front-end can be accessed using http://localhost:8080/ and log in with 'admin' for both your Username and Password.

What should I gather from this example
=================================

1. You can run a KubernetesPodOperator with a sidecar but it requires using a spec file like the one in `./pod_templates/sidecar_spec.yaml`
2. You have to do some unsavory things to get the sidecar to exit when you would like it to.
   1. In this example:
      1. I need the sidecar to live at least as long as the base pod
      2. I need the sidecar to continue running after the base pod if there is still work to be done (i.e. still files)
      3. I need the sidecar to die if there is no work left for the sidecar
   2. Why is this unsavory?:
      1. It relies on a file in a shared volume. Things could go wrong and it would be nicer to use another methodology.
   3. Are there other options you didn't explore:
      1. This could potentially be a great use-case for xcoms but I did not go that deep in this iteration.
      2. Its worth noting that the xcoms may bring a bit more stability than this methodology but there are also reliability issues with xcoms sometimes as well.

How was this example repo generated
=================================
1. I followed the docs [here](https://docs.astronomer.io/astro/install-cli) and [here](https://docs.astronomer.io/software/kubepodoperator-local).
2. Then I followed [this](https://docs.astronomer.io/astro/create-project) to initialize the project.