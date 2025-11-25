# 🚀 Deployment Checklist

## ✅ Before You Start
- [ ] GitHub repository is created and code is pushed
- [ ] All local environment variables are documented
- [ ] Railway account created
- [ ] Render account created
- [ ] Vercel account created

## 📦 Step 1: Railway (Database)
- [ ] MySQL database provisioned on Railway
- [ ] Database credentials copied
- [ ] DATABASE_URL constructed: `mysql+pymysql://USER:PASSWORD@HOST:PORT/DATABASE`
- [ ] Test connection from local machine (optional)

## 🔧 Step 2: Render (Backend)
- [ ] Web service created on Render
- [ ] GitHub repository connected
- [ ] Root directory set to `backend`
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] All environment variables added (see `.env.deployment.template`)
- [ ] `DATABASE_URL` updated with Railway credentials
- [ ] Service deployed successfully
- [ ] Database migrations run: `alembic upgrade head`
- [ ] Backend URL copied: `https://__________.onrender.com`
- [ ] Test API docs: `https://your-backend.onrender.com/docs`

## 🌐 Step 3: Vercel (Frontend)
- [ ] Project created on Vercel
- [ ] GitHub repository connected
- [ ] Root directory set to `frontend`
- [ ] Framework preset: Create React App
- [ ] Environment variable added: `REACT_APP_API_URL=https://your-backend.onrender.com`
- [ ] Deployed successfully
- [ ] Frontend URL copied: `https://__________.vercel.app`

## 🔄 Step 4: Update CORS
- [ ] Go back to Render
- [ ] Update `BACKEND_CORS_ORIGINS` with Vercel URL
- [ ] Update `FRONTEND_URL` with Vercel URL
- [ ] Save and redeploy

## ✨ Step 5: Test Everything
- [ ] Visit frontend URL
- [ ] Register new account
- [ ] Verify email received
- [ ] Login works
- [ ] Report lost item
- [ ] Report found item
- [ ] Upload images
- [ ] Browse items
- [ ] Test claim functionality
- [ ] Check admin panel (if admin user exists)

## 🎉 Deployment Complete!
Your app is live at:
- **Frontend**: https://__________.vercel.app
- **Backend**: https://__________.onrender.com
- **API Docs**: https://__________.onrender.com/docs

---

## 📝 Notes
- First request to Render may take ~30 seconds (cold start)
- Railway free tier: 500 hours/month
- Keep your SECRET_KEY secure!
- Monitor logs on each platform for errors
