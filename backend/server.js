const express = require('express');
const { createClient } = require('@supabase/supabase-js');
const { generateExamPaper } = require('./examGenerator');

const app = express();
app.use(express.json());

// Initialize Supabase using your project reference
const SUPABASE_URL = 'https://jakdpkzswcxcspoyoqck.supabase.co';
const SUPABASE_KEY = process.env.SUPABASE_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impha2Rwa3pzd2N4Y3Nwb3lvcWNrIiwicm9sZSI6ImFub24iOjE3ODY1NDA3MTQsImV4cCI6MjEwMjExNjcxNH0.jCnp-k_oZtHB0LveOZBbMvBSttu3ExoH9I_R5DjC0rc';

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

// API Endpoint to trigger exam generation based on user choices
app.post('/api/generate-exam', async (req, res) => {
    try {
        const { gradeLevel, subject, term, userSectionConfig } = req.body;

        // Call our core exam generator engine
        const examResult = await generateExamPaper(gradeLevel, subject, term, userSectionConfig);

        res.status(200).json({
            success: true,
            message: "Exam blueprint loaded and prompt generated successfully for Elevate Kenya Predictions.",
            data: examResult
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Elevate Kenya Exam Engine running on port ${PORT}`);
});
