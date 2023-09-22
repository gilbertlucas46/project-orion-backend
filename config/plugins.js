module.exports = ({ env }) => ({
  graphql: {
    enabled: true,
    config: {
      apolloServer: {
        introspection: true,
      },
      playgroundAlways: true,
    }
  },
  upload: {
    config: {
      provider: 'cloudinary',
      providerOptions: {
        cloud_name: process.env.CLOUDINARY_NAME,
        api_key: process.env.CLOUDINARY_KEY,
        api_secret: process.env.CLOUDINARY_SECRET,
      },
      actionOptions: {
        upload: {},
        uploadStream: {},
        delete: {},
      },
    },
  },
  ckeditor: {
    enabled: true,
    resolve: "./src/plugins/strapi-plugin-ckeditor"
  },
});

